import os
import time
import requests
import pandas as pd
import yfinance as yf
import pytz
import gspread
import google.auth
from io import StringIO
from datetime import datetime, timedelta
from google.cloud import bigquery
from dotenv import load_dotenv # Importante
from oauth2client.service_account import ServiceAccountCredentials
import warnings

warnings.filterwarnings("ignore")

# --- 1. CARGA DE VARIABLES DE ENTORNO ---
load_dotenv()

# --- 2. CONFIGURACIÓN DE DATOS (Centralizada en .env) ---
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_NAME")      # finance_data
TABLE_ID = os.getenv("BQ_TABLE_HISTORICO")     # sp500_history
SHEET_NAME = "pyroboadvisor" 
TAB_NAME = "EEUU_watchlist"

# --- 3. CONFIGURACIÓN TELEGRAM (Segura) ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") # Ojo: debe llamarse igual que en tu .env
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validación de seguridad (Para que no corra si faltan claves)
if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID or not PROJECT_ID:
    print("❌ ERROR CRÍTICO: Faltan variables en el archivo .env")
    print("   Verifica: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID y GCP_PROJECT_ID")
    exit(1)

# --- INICIALIZACIÓN CLIENTE BIGQUERY ---
try:
    client = bigquery.Client(project=PROJECT_ID)
except Exception as e:
    print(f"❌ Error cliente BigQuery: {e}")
    exit(1)

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=data)
    except Exception as e:
        print(f"⚠️ Error Telegram: {e}")

def get_sp500_tickers():
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        df = pd.read_html(StringIO(r.text))[0]
        return [t.replace('.', '-') for t in df['Symbol'].values]
    except Exception as e:
        send_telegram_msg(f"⚠️ Error Wikipedia: {e}")
        return []

def get_personal_tickers():
    print(f"🔐 Leyendo hoja '{TAB_NAME}'...")
    try:
        # Usamos google.auth en lugar de buscar un archivo .json
        scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials, _ = google.auth.default(scopes=scopes)
        
        gc = gspread.authorize(credentials)
        sh = gc.open(SHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)
        
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)
        df.columns = [c.lower().strip() for c in df.columns]
        
        if 'ticker' in df.columns:
            return [str(t).strip().upper().replace('.', '-') for t in df['ticker'].values if str(t).strip() != '']
        else:
            send_telegram_msg("⚠️ Alerta: Columna 'ticker' no encontrada en Excel.")
            return []
    except Exception as e:
        send_telegram_msg(f"❌ Error Excel: {e}")
        return []
    

def get_existing_tickers_in_bq():
    query = f"SELECT DISTINCT Ticker FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
    try:
        df = client.query(query).to_dataframe()
        return df['Ticker'].tolist()
    except:
        return []

def get_last_saved_date():
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    try:
        sql = f"SELECT MAX(Date) as last_date FROM `{table_ref}`"
        results = client.query(sql).result()
        for row in results: return row.last_date
    except: return None

def process_data(data_df):
    if data_df.empty: return pd.DataFrame()
    try:
        if isinstance(data_df.columns, pd.MultiIndex):
            stack = data_df.stack(level=0).reset_index()
            stack.rename(columns={'level_1': 'Ticker'}, inplace=True)
        else:
            stack = data_df.reset_index()
            stack['Ticker'] = data_df.columns.name if data_df.columns.name else 'UNKNOWN'

        cols_map = {'Date': 'Date', 'Close': 'Price', 'Volume': 'Volume'}
        if 'Adj Close' in stack.columns: cols_map['Adj Close'] = 'Price'
        stack = stack.rename(columns=cols_map)
        
        if 'Price' not in stack.columns: stack['Price'] = stack.get('Close', 0.0)
        
        final_df = stack[['Date', 'Ticker', 'Price', 'Volume']].dropna().copy()
        final_df['Date'] = final_df['Date'].dt.date
        final_df['Ticker'] = final_df['Ticker'].astype(str)
        final_df['Price'] = final_df['Price'].astype(float)
        final_df['Volume'] = final_df['Volume'].astype(int)
        return final_df
    except:
        return pd.DataFrame()

def download_batch(tickers, start_date):
    if not tickers: return pd.DataFrame()
    print(f"   ⬇️ Descargando {len(tickers)} activos desde {start_date}...")
    try:
        d = yf.download(tickers, start=start_date, group_by='ticker', auto_adjust=True, threads=False, progress=False)
        return process_data(d)
    except:
        return pd.DataFrame()

def main():
    start_time = time.time()
    
    print(f"🚀 Iniciando Pipeline...")
    tz = pytz.timezone('America/New_York')
    today = datetime.now(tz).date()
    
    # --- LÓGICA DE FIN DE SEMANA ---
    if today.weekday() > 4:
        print("🛑 Fin de semana detectado.")
        
        # Calculamos tiempo (será casi 0, pero confirma ejecución)
        end_time = time.time()
        duration_sec = end_time - start_time
        
        msg_weekend = (
             f"✅ *Monitor Activo (Fin de Semana)*\n"
             f"📅 Fecha: {today}\n"
             f"⏱️ Duración: {duration_sec:.2f}s\n"
             f"📂 Tabla: \n"
             f"😴 Estado: Mercado cerrado. Sin cambios en BD."
        )
        send_telegram_msg(msg_weekend)
        return # <--- AQUÍ TERMINA SI ES SÁBADO/DOMINGO

    # --- LÓGICA DE LUNES A VIERNES ---
    sp500 = get_sp500_tickers()
    personal = get_personal_tickers()
    all_targets = list(set(sp500 + personal))
    
    existing_in_bq = get_existing_tickers_in_bq()
    new_tickers = [t for t in all_targets if t not in existing_in_bq]
    old_tickers = [t for t in all_targets if t in existing_in_bq]

    final_data = pd.DataFrame()
    dfs_to_concat = []

    if new_tickers:
        df_new = download_batch(new_tickers, start_date="2020-01-01")
        if not df_new.empty: dfs_to_concat.append(df_new)

    if old_tickers:
        last_date = get_last_saved_date()
        if last_date:
            start_inc = last_date + timedelta(days=1)
            if start_inc <= today:
                df_old = download_batch(old_tickers, start_date=start_inc)
                if not df_old.empty: dfs_to_concat.append(df_old)
        else:
            df_old = download_batch(old_tickers, start_date="2020-01-01")
            if not df_old.empty: dfs_to_concat.append(df_old)

    if dfs_to_concat:
        final_data = pd.concat(dfs_to_concat)
    
    # Si es entre semana pero Yahoo falló o no hubo datos
    if final_data.empty:
        end_time = time.time()
        duration_sec = end_time - start_time
        minutes = int(duration_sec // 60)
        seconds = int(duration_sec % 60)
        
        msg_empty = (
            f"⚠️ *Reporte Sin Datos*\n"
            f"📅 Fecha: {today}\n"
            f"⏱️ Duración: {minutes}m {seconds}s\n"
            f"El robot corrió pero no encontró precios nuevos hoy."
        )
        send_telegram_msg(msg_empty)
        return

    print(f"📦 Guardando {len(final_data):,} registros...")
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Date", "DATE"),
            bigquery.SchemaField("Ticker", "STRING"),
            bigquery.SchemaField("Price", "FLOAT"),
            bigquery.SchemaField("Volume", "INTEGER"),
        ],
        write_disposition="WRITE_APPEND",
    )

    try:
        client.load_table_from_dataframe(final_data, table_ref, job_config=job_config).result()
        
        # ⏱️ REPORTE DE ÉXITO (ENTRE SEMANA)
        end_time = time.time()
        duration_sec = end_time - start_time
        minutes = int(duration_sec // 60)
        seconds = int(duration_sec % 60)

        msg_success = (
            f"✅ *Carga Exitosa*\n"
            f"📅 Fecha: {today}\n"
            f"⏱️ Duración: {minutes}m {seconds}s\n"
            f"📂 Tabla: \n"
            f"📊 Registros: {len(final_data):,}\n"
            f"🆕 Nuevos: {len(new_tickers)}"
        )
        send_telegram_msg(msg_success)
        print("✨ ¡Éxito Total!")
    except Exception as e:
        send_telegram_msg(f"❌ Error BigQuery: {str(e)}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
