"""
SP500 Finance ETL - Security Hardened Version
Fetches S&P 500 companies data and syncs to Google Sheets + BigQuery
"""

import os
import json
import re
from datetime import datetime, timedelta
from time import time
import pandas as pd
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import bigquery
import gspread

# Load environment variables
load_dotenv()

# =====================================
# CONFIGURATION & VALIDATION
# =====================================

def validate_env_vars():
    """Validate all required environment variables with format checking"""
    errors = []
    
    # Telegram Bot Token (format: numeric:alphanumeric)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or not re.match(r'^\d+:[A-Za-z0-9_-]+$', token):
        errors.append("TELEGRAM_BOT_TOKEN inválido (formato: 1234567890:ABCdef...)")
    
    # Telegram Chat ID (numeric, puede ser negativo)
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id or not chat_id.lstrip('-').isdigit():
        errors.append("TELEGRAM_CHAT_ID debe ser numérico")
    
    # GCP Project ID (lowercase alphanumeric + hyphens, 6-30 chars)
    project = os.getenv("GCP_PROJECT_ID")
    if not project or not re.match(r'^[a-z0-9-]{6,30}$', project):
        errors.append("GCP_PROJECT_ID inválido (6-30 caracteres, solo a-z0-9-)")
    
    # Google Sheets configuration
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    if not sheet_name or len(sheet_name) < 1:
        errors.append("GOOGLE_SHEET_NAME requerido")
    
    tab_name = os.getenv("GOOGLE_SHEET_TAB")
    if not tab_name or len(tab_name) < 1:
        errors.append("GOOGLE_SHEET_TAB requerido")
    
    # Service Account JSON path
    sa_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_path or not os.path.exists(sa_path):
        errors.append("GOOGLE_SERVICE_ACCOUNT_JSON no existe o no especificado")
    
    if errors:
        print("❌ ERROR CRÍTICO: Variables de entorno inválidas:\n")
        for err in errors:
            print(f"   - {err}")
        exit(1)
    
    return True

# Validate on startup
validate_env_vars()

# Load validated environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
TAB_NAME = os.getenv("GOOGLE_SHEET_TAB")
SA_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
CREDENTIALS_CREATED = os.getenv("CREDENTIALS_CREATED_DATE", "2026-03-26")

# =====================================
# TELEGRAM MESSAGING (Rate Limited)
# =====================================

last_message_time = 0

def send_telegram_msg(message, min_interval=2):
    """
    Send message to Telegram with rate limiting
    
    Args:
        message: Message text (sanitized, no sensitive data)
        min_interval: Minimum seconds between messages
    """
    global last_message_time
    
    current_time = time()
    if current_time - last_message_time < min_interval:
        print(f"⏳ Rate limit: esperando {min_interval}s antes de enviar")
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=5)
        response.raise_for_status()
        last_message_time = current_time
        print(f"✅ Telegram: {message[:50]}...")
    except requests.exceptions.Timeout:
        print("⚠️ Telegram timeout (5s)")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Telegram error: {type(e).__name__}")

# =====================================
# CREDENTIALS ROTATION CHECK
# =====================================

def check_credentials_age():
    """Alert if credentials are older than 90 days"""
    try:
        cred_date = datetime.strptime(CREDENTIALS_CREATED, "%Y-%m-%d")
        age_days = (datetime.now() - cred_date).days
        
        if age_days > 90:
            send_telegram_msg(
                f"⚠️ <b>ALERTA SEGURIDAD</b>\n\n"
                f"Credenciales tienen {age_days} días.\n"
                f"Recomendado: Rotar cada 90 días."
            )
        elif age_days > 75:
            send_telegram_msg(
                f"🟡 Credenciales expiran pronto: {age_days}/90 días"
            )
    except ValueError:
        print("⚠️ CREDENTIALS_CREATED_DATE inválido en .env")

# =====================================
# DATA FETCHING
# =====================================

def fetch_sp500_from_wikipedia():
    """
    Fetch S&P 500 companies list from Wikipedia
    
    Returns:
        pandas.DataFrame: Company data
    """
    print("📡 Fetching S&P 500 from Wikipedia...")
    
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {
        'User-Agent': 'Mozilla/5.0 (SP500-ETL-Bot/1.0)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        tables = pd.read_html(response.text)
        df = tables[0]
        
        print(f"✅ Fetched {len(df)} companies")
        return df
        
    except requests.exceptions.Timeout:
        send_telegram_msg("⚠️ Wikipedia timeout (10s)")
        raise
    except requests.exceptions.RequestException as e:
        send_telegram_msg("⚠️ Error conectando a Wikipedia")
        print(f"Error detail: {type(e).__name__}")
        raise

# =====================================
# GOOGLE SHEETS SYNC
# =====================================

def sync_to_google_sheets(df):
    """
    Sync DataFrame to Google Sheets using service account
    
    Args:
        df: pandas.DataFrame to upload
    """
    print(f"🔐 Conectando a Google Sheets (SA: {SA_PATH})...")
    
    try:
        # Use service account credentials (more secure)
        scopes = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = service_account.Credentials.from_service_account_file(
            SA_PATH,
            scopes=scopes
        )
        
        gc = gspread.authorize(credentials)
        
        print(f"📊 Abriendo hoja '{SHEET_NAME}' / tab '{TAB_NAME}'...")
        sh = gc.open(SHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)
        
        # Clear and update
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        print(f"✅ Google Sheets actualizado: {len(df)} filas")
        send_telegram_msg(
            f"✅ <b>Google Sheets actualizado</b>\n"
            f"Filas: {len(df)}"
        )
        
    except FileNotFoundError:
        send_telegram_msg("❌ Service account file no encontrado")
        raise
    except gspread.exceptions.SpreadsheetNotFound:
        send_telegram_msg(f"❌ Hoja '{SHEET_NAME}' no encontrada")
        raise
    except Exception as e:
        # Log detailed error locally, send generic message
        print(f"❌ Google Sheets error detail: {type(e).__name__}: {str(e)}")
        send_telegram_msg("❌ Error al actualizar Google Sheets")
        raise

# =====================================
# BIGQUERY SYNC
# =====================================

def sync_to_bigquery(df):
    """
    Sync DataFrame to BigQuery
    
    Args:
        df: pandas.DataFrame to upload
    """
    print(f"🔐 Conectando a BigQuery (project: {PROJECT_ID})...")
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SA_PATH
        )
        
        client = bigquery.Client(
            credentials=credentials,
            project=PROJECT_ID
        )
        
        table_id = f"{PROJECT_ID}.finance_data.sp500_companies"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        job.result()
        
        print(f"✅ BigQuery actualizado: {len(df)} filas")
        send_telegram_msg(
            f"✅ <b>BigQuery actualizado</b>\n"
            f"Tabla: sp500_companies\n"
            f"Filas: {len(df)}"
        )
        
    except Exception as e:
        print(f"❌ BigQuery error detail: {type(e).__name__}: {str(e)}")
        send_telegram_msg("❌ Error al actualizar BigQuery")
        raise

# =====================================
# MAIN EXECUTION
# =====================================

def main():
    """Main ETL pipeline"""
    print("\n" + "="*50)
    print("🚀 SP500 Finance ETL - Starting")
    print("="*50 + "\n")
    
    # Check credentials age
    check_credentials_age()
    
    try:
        # 1. Fetch data
        df = fetch_sp500_from_wikipedia()
        
        # 2. Sync to Google Sheets
        sync_to_google_sheets(df)
        
        # 3. Sync to BigQuery
        sync_to_bigquery(df)
        
        print("\n" + "="*50)
        print("✅ ETL COMPLETADO EXITOSAMENTE")
        print("="*50 + "\n")
        
        send_telegram_msg(
            "✅ <b>SP500 ETL Completado</b>\n\n"
            f"Empresas procesadas: {len(df)}\n"
            f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
    except Exception as e:
        print(f"\n❌ ETL FAILED: {type(e).__name__}")
        send_telegram_msg(
            "❌ <b>SP500 ETL FAILED</b>\n\n"
            "Revisa logs para detalles"
        )
        raise

if __name__ == "__main__":
    main()
