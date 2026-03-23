# 🛠️ Setup Guide - S&P 500 Finance ETL

## 🇬🇧 Installation Guide

This guide walks you through setting up the S&P 500 Finance ETL pipeline from scratch, including all prerequisites and configuration steps.

---

## 🇪🇸 Guía de Instalación

Esta guía te llevará paso a paso en la configuración del pipeline S&P 500 Finance ETL desde cero, incluyendo todos los prerrequisitos y pasos de configuración.

---

## 📋 Prerequisites / Prerrequisitos

### 🇬🇧 Required

1. **Python 3.8 or higher**
   - Check version: `python --version`
   - Install from [python.org](https://www.python.org/downloads/)

2. **Google Cloud Platform Account**
   - Sign up at [cloud.google.com](https://cloud.google.com/)
   - Enable billing (free tier available)

3. **Git** (for cloning repository)
   - Check: `git --version`
   - Install: [git-scm.com](https://git-scm.com/)

### 🇪🇸 Requerido

1. **Python 3.8 o superior**
   - Verificar versión: `python --version`
   - Instalar desde [python.org](https://www.python.org/downloads/)

2. **Cuenta de Google Cloud Platform**
   - Registrarse en [cloud.google.com](https://cloud.google.com/)
   - Habilitar facturación (tier gratuito disponible)

3. **Git** (para clonar el repositorio)
   - Verificar: `git --version`
   - Instalar: [git-scm.com](https://git-scm.com/)

### 🇬🇧 Optional (but Recommended)

- **Telegram Bot** (for pipeline notifications)
- **Google Sheets** (for custom watchlists)

### 🇪🇸 Opcional (pero Recomendado)

- **Bot de Telegram** (para notificaciones del pipeline)
- **Google Sheets** (para listas de seguimiento personalizadas)

---

## 🚀 Step 1: Clone Repository / Clonar Repositorio

```bash
# Clone the repository / Clonar el repositorio
git clone https://github.com/darmasatext/sp500-finance-etl.git
cd sp500-finance-etl

# Create virtual environment / Crear entorno virtual
python -m venv venv

# Activate virtual environment / Activar entorno virtual
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

---

## 📦 Step 2: Install Dependencies / Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Dependencies List / Lista de Dependencias

```
pandas              # Data manipulation / Manipulación de datos
yfinance            # Yahoo Finance API / API de Yahoo Finance
google-cloud-bigquery  # BigQuery client / Cliente BigQuery
google-auth         # GCP authentication / Autenticación GCP
gspread             # Google Sheets API / API de Google Sheets
python-dotenv       # Environment variables / Variables de entorno
requests            # HTTP requests / Peticiones HTTP
lxml                # HTML parsing / Análisis HTML
pandas-gbq          # Pandas BigQuery integration / Integración Pandas-BigQuery
pytz                # Timezone handling / Manejo de zonas horarias
oauth2client        # OAuth 2.0 authentication / Autenticación OAuth 2.0
```

---

## ☁️ Step 3: Configure Google Cloud Platform

### 🇬🇧 3.1 Create GCP Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter project name (e.g., `finance-etl-prod`)
4. Note your **Project ID** (you'll need this later)

### 🇪🇸 3.1 Crear Proyecto GCP

1. Ir a [console.cloud.google.com](https://console.cloud.google.com/)
2. Clic en **"Seleccionar proyecto"** → **"Proyecto nuevo"**
3. Ingresar nombre del proyecto (ej., `finance-etl-prod`)
4. Anotar tu **ID del Proyecto** (lo necesitarás después)

---

### 🇬🇧 3.2 Enable Required APIs

```bash
# Enable BigQuery API / Habilitar API de BigQuery
gcloud services enable bigquery.googleapis.com

# Enable Sheets API (if using custom watchlists)
gcloud services enable sheets.googleapis.com

# Enable Drive API (for Sheets access)
gcloud services enable drive.googleapis.com
```

**Or via Console**:
1. Go to **APIs & Services** → **Library**
2. Search and enable:
   - BigQuery API
   - Google Sheets API (optional)
   - Google Drive API (optional)

### 🇪🇸 3.2 Habilitar APIs Requeridas

**O vía Consola**:
1. Ir a **APIs y Servicios** → **Biblioteca**
2. Buscar y habilitar:
   - BigQuery API
   - API de Google Sheets (opcional)
   - API de Google Drive (opcional)

---

### 🇬🇧 3.3 Create BigQuery Dataset

```bash
# Create dataset / Crear dataset
bq mk --dataset \
  --location=US \
  --description="S&P 500 Finance Data" \
  YOUR_PROJECT_ID:finance_data
```

**Or via Console**:
1. Go to **BigQuery** → **SQL Workspace**
2. Click **"Create Dataset"**
3. Dataset ID: `finance_data`
4. Location: `US` (or your preferred region)

### 🇪🇸 3.3 Crear Dataset de BigQuery

**O vía Consola**:
1. Ir a **BigQuery** → **Espacio de trabajo SQL**
2. Clic en **"Crear conjunto de datos"**
3. ID del conjunto: `finance_data`
4. Ubicación: `US` (o tu región preferida)

---

### 🇬🇧 3.4 Setup Authentication

**Option A: Service Account (Recommended for Production)**

```bash
# Create service account
gcloud iam service-accounts create finance-etl-sa \
  --display-name="Finance ETL Service Account"

# Grant BigQuery permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:finance-etl-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:finance-etl-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

# Create and download key
gcloud iam service-accounts keys create credentials.json \
  --iam-account=finance-etl-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```

**Option B: User Account (for Development)**

```bash
# Login with your Google account
gcloud auth application-default login

# Credentials will be stored at:
# ~/.config/gcloud/application_default_credentials.json
```

### 🇪🇸 3.4 Configurar Autenticación

**Opción A: Cuenta de Servicio (Recomendado para Producción)**

*(Ver comandos arriba)*

**Opción B: Cuenta de Usuario (para Desarrollo)**

```bash
# Iniciar sesión con tu cuenta de Google
gcloud auth application-default login

# Las credenciales se guardarán en:
# ~/.config/gcloud/application_default_credentials.json
```

---

### 🇬🇧 3.5 Setup Google Sheets Access (Optional)

If you want to use custom watchlists from Google Sheets:

1. **Enable Google Sheets API** (Step 3.2)
2. **Grant Sheets access to your service account**:
   - Open your Google Sheet
   - Click **Share**
   - Add email: `finance-etl-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com`
   - Grant **Editor** access

3. **Configure Sheet details in code**:
   Edit `maestro_tickers.py`:
   ```python
   SHEET_NAME = "your-sheet-name"
   TAB_NAME = "your-tab-name"
   ```

### 🇪🇸 3.5 Configurar Acceso a Google Sheets (Opcional)

Si deseas usar listas personalizadas desde Google Sheets:

1. **Habilitar API de Google Sheets** (Paso 3.2)
2. **Otorgar acceso Sheets a tu cuenta de servicio**:
   - Abrir tu Google Sheet
   - Clic en **Compartir**
   - Agregar email: `finance-etl-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com`
   - Otorgar acceso de **Editor**

3. **Configurar detalles de la hoja en el código**:
   Editar `maestro_tickers.py`:
   ```python
   SHEET_NAME = "nombre-de-tu-hoja"
   TAB_NAME = "nombre-de-tu-pestaña"
   ```

---

## 📱 Step 4: Configure Telegram Notifications (Optional)

### 🇬🇧 4.1 Create Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow instructions to name your bot
4. Save the **Bot Token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 🇪🇸 4.1 Crear Bot de Telegram

1. Abrir Telegram y buscar **@BotFather**
2. Enviar comando `/newbot`
3. Seguir instrucciones para nombrar tu bot
4. Guardar el **Token del Bot** (se ve como `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

### 🇬🇧 4.2 Get Chat ID

1. Start a chat with your new bot
2. Send any message (e.g., "Hello")
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for `"chat":{"id":123456789}` in the JSON response
5. Save this **Chat ID**

### 🇪🇸 4.2 Obtener Chat ID

1. Iniciar chat con tu nuevo bot
2. Enviar cualquier mensaje (ej., "Hola")
3. Visitar: `https://api.telegram.org/bot<TU_TOKEN_BOT>/getUpdates`
4. Buscar `"chat":{"id":123456789}` en la respuesta JSON
5. Guardar este **Chat ID**

---

## ⚙️ Step 5: Configure Environment Variables

### 🇬🇧 Create `.env` File

Create a `.env` file in the project root:

```bash
# Copy template / Copiar plantilla
cp .env.example .env

# Edit with your values / Editar con tus valores
nano .env
```

### .env File Contents / Contenido del Archivo .env

```env
# ==============================
# Google Cloud Platform Config
# ==============================
GCP_PROJECT_ID=your-project-id-here
BQ_DATASET_NAME=finance_data
BQ_TABLE_MAESTRA=sp500_tickers
BQ_TABLE_HISTORICO=sp500_history
BQ_TABLE_INFO=sp500_tickers_info

# ==============================
# Telegram Notifications (Optional)
# ==============================
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# ==============================
# Google Sheets (Optional)
# ==============================
# Configure in maestro_tickers.py:
# SHEET_NAME = "your-sheet-name"
# TAB_NAME = "your-tab-name"
```

### 🇪🇸 Crear Archivo `.env`

*(Ver contenido arriba)*

**⚠️ Important / Importante**: Never commit `.env` to version control! / ¡Nunca subir `.env` al control de versiones!

```bash
# Add to .gitignore / Agregar a .gitignore
echo ".env" >> .gitignore
echo "credentials.json" >> .gitignore
```

---

## ✅ Step 6: Verify Setup / Verificar Configuración

### 🇬🇧 Test Authentication

```bash
# Test BigQuery connection
python -c "from google.cloud import bigquery; client = bigquery.Client(); print('✅ BigQuery connected!')"

# Test environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Project:', os.getenv('GCP_PROJECT_ID'))"
```

### 🇪🇸 Probar Autenticación

*(Ver comandos arriba)*

---

### 🇬🇧 Test Individual Components

```bash
# Test master catalog update
python maestro_tickers.py

# Test historical data sync (will process delta)
python historico_final.py

# Test fundamentals update
python perfil_fundamental.py

# Test notifications
python notificaciones.py
```

Expected output should include:
- ✅ Success messages
- No ❌ error messages
- BigQuery row counts

### 🇪🇸 Probar Componentes Individuales

*(Ver comandos arriba)*

Salida esperada debe incluir:
- ✅ Mensajes de éxito
- Sin mensajes ❌ de error
- Contadores de filas en BigQuery

---

## 🔄 Step 7: Run Full Pipeline / Ejecutar Pipeline Completo

```bash
python pipeline.py
```

**🇬🇧 Expected Duration**: 2-5 minutes (first run may take 10-15 minutes for historical backfill)

**🇪🇸 Duración Esperada**: 2-5 minutos (primera ejecución puede tomar 10-15 minutos para el backfill histórico)

### Success Indicators / Indicadores de Éxito

- ✅ All stages complete without errors
- 📱 Telegram notification received (if configured)
- 📊 Data visible in BigQuery console
- ⏱️ Pipeline duration logged

---

## 📅 Step 8: Schedule Automated Runs

### 🇬🇧 Option A: Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add daily execution at 3:15 PM CST (Mon-Fri)
15 15 * * 1-5 cd /path/to/sp500-finance-etl && /path/to/venv/bin/python pipeline.py >> /var/log/finance-etl.log 2>&1
```

### 🇪🇸 Opción A: Cron (Linux/Mac)

*(Ver comandos arriba)*

---

### 🇬🇧 Option B: Cloud Scheduler (GCP)

```bash
# Create Cloud Run job (if using Cloud Run)
gcloud run deploy finance-etl \
  --source . \
  --region us-central1 \
  --no-allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=your-project-id

# Create scheduler job
gcloud scheduler jobs create http finance-etl-daily \
  --schedule="15 15 * * 1-5" \
  --time-zone="America/Chicago" \
  --uri="https://finance-etl-XXXXX-uc.a.run.app" \
  --http-method=POST \
  --oidc-service-account-email=finance-etl-sa@your-project-id.iam.gserviceaccount.com
```

### 🇪🇸 Opción B: Cloud Scheduler (GCP)

*(Ver comandos arriba)*

---

### 🇬🇧 Option C: Task Scheduler (Windows)

1. Open **Task Scheduler**
2. Create Basic Task
3. Trigger: Daily at 3:15 PM, weekdays only
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `pipeline.py`
   - Start in: `C:\path\to\sp500-finance-etl`

### 🇪🇸 Opción C: Programador de Tareas (Windows)

1. Abrir **Programador de Tareas**
2. Crear Tarea Básica
3. Desencadenador: Diario a las 3:15 PM, solo días laborables
4. Acción: Iniciar un programa
   - Programa: `C:\ruta\a\venv\Scripts\python.exe`
   - Argumentos: `pipeline.py`
   - Iniciar en: `C:\ruta\a\sp500-finance-etl`

---

## 🐛 Troubleshooting / Solución de Problemas

### 🇬🇧 Common Issues

#### Error: "Could not automatically determine credentials"

**Solution**:
```bash
# Set credentials explicitly
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# Or login with user account
gcloud auth application-default login
```

#### Error: "403 BigQuery permission denied"

**Solution**: Grant required roles to service account:
```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:finance-etl-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"
```

#### Error: "Yahoo Finance timeout / no data"

**Solution**: 
- Check internet connection
- Verify ticker symbols are valid
- Add problematic tickers to `TICKERS_IGNORAR` list in `historico_final.py`

#### Error: "Telegram notification failed"

**Solution**:
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- Test bot connection: visit `https://api.telegram.org/bot<TOKEN>/getMe`
- Ensure chat was started with bot before getting Chat ID

### 🇪🇸 Problemas Comunes

*(Ver soluciones arriba - mismos comandos aplican)*

---

## 🔒 Security Best Practices / Mejores Prácticas de Seguridad

### 🇬🇧 Recommendations

1. **Never commit secrets to Git**
   ```bash
   # Always in .gitignore:
   .env
   credentials.json
   *.key
   ```

2. **Use service accounts for production**
   - Principle of least privilege
   - Grant only required roles

3. **Rotate credentials regularly**
   - Service account keys: every 90 days
   - Telegram bot tokens: if compromised

4. **Restrict BigQuery access**
   - Use dataset-level permissions
   - Consider column-level security for sensitive data

5. **Enable audit logging**
   ```bash
   gcloud logging read "resource.type=bigquery_resource" --limit 50
   ```

### 🇪🇸 Recomendaciones

*(Ver lista arriba - aplica para todos)*

---

## 📊 Verify Data in BigQuery

### 🇬🇧 Run Test Queries

```sql
-- Check ticker count
SELECT COUNT(DISTINCT Ticker) as total_tickers
FROM `your-project.finance_data.sp500_tickers`;

-- Check historical data
SELECT 
  Ticker,
  COUNT(*) as days,
  MIN(Date) as first_date,
  MAX(Date) as last_date
FROM `your-project.finance_data.sp500_history`
GROUP BY Ticker
ORDER BY days DESC
LIMIT 10;

-- Check fundamentals
SELECT 
  Ticker,
  Company_Name,
  Sector,
  Market_Cap,
  PE_Ratio,
  Last_Updated
FROM `your-project.finance_data.sp500_tickers_info`
WHERE Market_Cap IS NOT NULL
ORDER BY Market_Cap DESC
LIMIT 10;
```

### 🇪🇸 Ejecutar Consultas de Prueba

*(Ver consultas SQL arriba)*

---

## 🎉 Next Steps / Próximos Pasos

### 🇬🇧 You're Ready!

The pipeline is now configured and ready to run. Next steps:

1. **Monitor first few runs** to ensure stability
2. **Review BigQuery data** to verify completeness
3. **Set up dashboards** (Looker Studio, Tableau, etc.)
4. **Explore Phase 2 features** in [FUTURE.md](./FUTURE.md)

### 🇪🇸 ¡Estás Listo!

El pipeline ahora está configurado y listo para ejecutarse. Próximos pasos:

1. **Monitorear primeras ejecuciones** para asegurar estabilidad
2. **Revisar datos en BigQuery** para verificar completitud
3. **Configurar dashboards** (Looker Studio, Tableau, etc.)
4. **Explorar características Fase 2** en [FUTURE.md](./FUTURE.md)

---

## 📚 Additional Resources / Recursos Adicionales

- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Google Sheets API Guide](https://developers.google.com/sheets/api)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Last Updated**: March 2026
