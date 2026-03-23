# 🇬🇧 🇪🇸 S&P 500 Finance ETL Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![BigQuery](https://img.shields.io/badge/BigQuery-Enabled-4285F4.svg)](https://cloud.google.com/bigquery)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4.svg)](https://telegram.org/)

---

## 🇬🇧 Overview

**S&P 500 Finance ETL** is an automated data pipeline that extracts, transforms, and loads financial data from the S&P 500 index and custom watchlists into Google BigQuery for analysis and reporting.

### Key Features

- 📊 **Automated Data Collection**: Daily scraping of S&P 500 constituents from Wikipedia
- 📈 **Historical Data Pipeline**: 5-year price history via Yahoo Finance API
- 💼 **Fundamental Analysis**: Company profiles with PE ratios, Beta, sectors, and dividends
- 🔄 **Delta Processing**: Incremental updates for efficient resource usage
- 📱 **Telegram Notifications**: Real-time pipeline status reports
- 🗓️ **Smart Scheduling**: Runs daily at 3:15 PM CST (market days only)
- 📝 **Custom Watchlists**: Integration with Google Sheets for personal tickers

### Architecture

```
Wikipedia (S&P 500) ──┐
                      ├──> Maestro Tickers ──> BigQuery (sp500_tickers)
Google Sheets ────────┘                              │
                                                     │
                                                     ▼
                                          Historico (Delta Check)
                                                     │
                                                     ▼
                                          Yahoo Finance (5y data)
                                                     │
                                                     ▼
                                          BigQuery (sp500_history)
                                                     │
                                                     ▼
                                          Perfil Fundamental
                                                     │
                                                     ▼
                                          BigQuery (sp500_tickers_info)
                                                     │
                                                     ▼
                                          Telegram Notification
```

---

## 🇪🇸 Resumen

**S&P 500 Finance ETL** es un pipeline automatizado que extrae, transforma y carga datos financieros del índice S&P 500 y listas personalizadas hacia Google BigQuery para análisis y reportes.

### Características Principales

- 📊 **Recolección Automatizada**: Scraping diario de los componentes del S&P 500 desde Wikipedia
- 📈 **Pipeline de Históricos**: 5 años de historial de precios vía API de Yahoo Finance
- 💼 **Análisis Fundamental**: Perfiles de empresas con ratios PE, Beta, sectores y dividendos
- 🔄 **Procesamiento Delta**: Actualizaciones incrementales para uso eficiente de recursos
- 📱 **Notificaciones Telegram**: Reportes en tiempo real del estado del pipeline
- 🗓️ **Programación Inteligente**: Se ejecuta diariamente a las 3:15 PM CST (sólo días de mercado)
- 📝 **Listas Personalizadas**: Integración con Google Sheets para tickers personales

---

## 🚀 Quick Start

### Prerequisites / Prerequisitos

- Python 3.8+
- Google Cloud Platform account with BigQuery enabled
- Telegram Bot Token (optional for notifications)
- Google Sheets API access (for custom watchlists)

### Installation / Instalación

```bash
# Clone repository / Clonar repositorio
git clone <repository-url>
cd sp500-finance-etl

# Install dependencies / Instalar dependencias
pip install -r requirements.txt

# Configure environment / Configurar entorno
cp .env.example .env
# Edit .env with your credentials / Editar .env con tus credenciales
```

### Configuration / Configuración

Create a `.env` file with the following variables:

```env
# Google Cloud Platform
GCP_PROJECT_ID=your-project-id
BQ_DATASET_NAME=finance_data
BQ_TABLE_MAESTRA=sp500_tickers
BQ_TABLE_HISTORICO=sp500_history
BQ_TABLE_INFO=sp500_tickers_info

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

### Run Pipeline / Ejecutar Pipeline

```bash
# Full pipeline / Pipeline completo
python pipeline.py

# Individual components / Componentes individuales
python maestro_tickers.py    # Update master catalog / Actualizar catálogo maestro
python historico_final.py     # Sync historical data / Sincronizar datos históricos
python perfil_fundamental.py  # Update fundamentals / Actualizar fundamentales
```

---

## 📚 Documentation / Documentación

- [**ARCHITECTURE.md**](./ARCHITECTURE.md) - System design and pipeline flow / Diseño del sistema y flujo del pipeline
- [**SETUP.md**](./SETUP.md) - Detailed installation guide / Guía de instalación detallada
- [**FUTURE.md**](./FUTURE.md) - Upcoming enhancements / Mejoras futuras
- [**docs/DATA_SCHEMA.md**](./docs/DATA_SCHEMA.md) - BigQuery table schemas / Esquemas de tablas BigQuery

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Data Warehouse | Google BigQuery |
| Data Source | Yahoo Finance, Wikipedia |
| Custom Lists | Google Sheets API |
| Notifications | Telegram Bot API |
| Scheduling | Cloud Scheduler / Cron |
| Authentication | Google Application Default Credentials |

---

## 📈 Future Enhancements / Mejoras Futuras

🔮 **Phase 2 - Technical Indicators** (Coming Soon / Próximamente)

The pipeline will be enhanced with advanced technical analysis indicators:
- Moving Averages (SMA, EMA)
- Relative Strength Index (RSI)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volume-based indicators

See [FUTURE.md](./FUTURE.md) for detailed roadmap.

---

## 📝 License / Licencia

MIT License - see [LICENSE](./LICENSE) file for details

Copyright (c) 2025 Diego Armas (@darmasatext)

---

## 👤 Author / Autor

**Diego Armas** (@darmasatext)

- Twitter: [@darmasatext](https://twitter.com/darmasatext)
- GitHub: [@darmasatext](https://github.com/darmasatext)

---

## 🙏 Acknowledgments / Agradecimientos

- Yahoo Finance for providing free financial data APIs
- Wikipedia for maintaining the S&P 500 constituent list
- Google Cloud Platform for BigQuery infrastructure

---

**Last Updated / Última Actualización**: March 2026
