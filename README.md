# 🇬🇧 🇪🇸 S&P 500 Finance ETL Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![BigQuery](https://img.shields.io/badge/BigQuery-Enabled-4285F4.svg)](https://cloud.google.com/bigquery)
[![Cloud Run](https://img.shields.io/badge/Cloud%20Run-Ready-4285F4.svg)](https://cloud.google.com/run)
[![Cost](https://img.shields.io/badge/Cost-$0%2Fmo-success.svg)](https://cloud.google.com/pricing)

---

## 🇬🇧 English

### Overview

**S&P 500 Finance ETL** is an automated data pipeline that extracts, transforms, and loads financial data from the S&P 500 index and custom watchlists into Google BigQuery for analysis and reporting.

**Design Philosophy:** Zero-cost, scalable, and production-ready.

### Key Features

- 📊 **Automated Data Collection**: Daily scraping of S&P 500 constituents from Wikipedia
- 📈 **Historical Data Pipeline**: 5-year price history via Yahoo Finance API
- 💼 **Fundamental Analysis**: Company profiles with PE ratios, Beta, sectors, and dividends
- 🔄 **Delta Processing**: Incremental updates for efficient resource usage
- 📱 **Telegram Notifications**: Real-time pipeline status reports
- 🗓️ **Smart Scheduling**: Runs daily at 3:15 PM CST (market days only)
- 📝 **Custom Watchlists**: Integration with Google Sheets for personal tickers
- 💰 **Zero Cost**: 100% within Google Cloud free tier

### 💰 Cost Breakdown

**Monthly Operating Cost: $0.00/month** 🎉

| Service | Usage | Cost |
|---------|-------|------|
| **Cloud Run Jobs** | 1 execution/day × 30 days = 30 jobs/month | **$0** (free tier: 180k vCPU-seconds/month) |
| **Cloud Scheduler** | 1 job configured | **$0** (free tier: 3 jobs) |
| **BigQuery Storage** | <0.5 GB (500 tickers × 3 tables × 5 years) | **$0** (free tier: 10 GB) |
| **BigQuery Queries** | ~50 MB processed/day | **$0** (free tier: 1 TB/month) |
| **Yahoo Finance API** | Free tier (no API key required) | **$0** |
| **Google Sheets API** | Minimal reads | **$0** (free tier: 100 requests/100s) |
| **Networking** | Egress negligible | **$0** |

**Total: $0.00/month** 💚

**Design Metrics:**
- ✅ **Zero Cost**: 100% within GCP free tier limits
- ✅ **Scalable**: Handles 1000+ tickers without infrastructure changes
- ✅ **Low Latency**: Incremental delta processing (only new/changed data)
- ✅ **Production Ready**: Automated, monitored, reliable

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

### Roadmap

See [FUTURE.md](./FUTURE.md) for planned enhancements:
- **Phase 2**: 6 basic technical indicators (RSI, SMA, Volume) - Q3 2026
- **Phase 3**: 9 advanced indicators (MACD, Bollinger Bands, EMA) - Q4 2026
- **Phase 4**: ML features + composite signals - Q1 2027
- **Phase 5**: OpenClaw Skill investment assistant - Q2 2027

### Quick Start

```bash
# Clone repository
git clone https://github.com/darmasatext/sp500-finance-etl
cd sp500-finance-etl

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run pipeline
python src/main.py
```

### Documentation

- [**SETUP.md**](./SETUP.md) - Detailed installation guide
- [**ARCHITECTURE.md**](./ARCHITECTURE.md) - System design and pipeline flow
- [**FUTURE.md**](./FUTURE.md) - Upcoming enhancements
- [**docs/DATA_SCHEMA.md**](./docs/DATA_SCHEMA.md) - BigQuery table schemas

### License

MIT License - Copyright (c) 2026 Diego Armas

---

## 🇪🇸 Español

### Resumen

**S&P 500 Finance ETL** es un pipeline automatizado que extrae, transforma y carga datos financieros del índice S&P 500 y listas personalizadas hacia Google BigQuery para análisis y reportes.

**Filosofía de Diseño:** Costo cero, escalable y listo para producción.

### Características Principales

- 📊 **Recolección Automatizada**: Scraping diario de los componentes del S&P 500 desde Wikipedia
- 📈 **Pipeline de Históricos**: 5 años de historial de precios vía API de Yahoo Finance
- 💼 **Análisis Fundamental**: Perfiles de empresas con ratios PE, Beta, sectores y dividendos
- 🔄 **Procesamiento Delta**: Actualizaciones incrementales para uso eficiente de recursos
- 📱 **Notificaciones Telegram**: Reportes en tiempo real del estado del pipeline
- 🗓️ **Programación Inteligente**: Se ejecuta diariamente a las 3:15 PM CST (sólo días de mercado)
- 📝 **Listas Personalizadas**: Integración con Google Sheets para tickers personales
- 💰 **Costo Cero**: 100% dentro del free tier de Google Cloud

### 💰 Desglose de Costos

**Costo Operacional Mensual: $0.00/mes** 🎉

| Servicio | Uso | Costo |
|----------|-----|-------|
| **Cloud Run Jobs** | 1 ejecución/día × 30 días = 30 jobs/mes | **$0** (free tier: 180k vCPU-segundos/mes) |
| **Cloud Scheduler** | 1 job configurado | **$0** (free tier: 3 jobs) |
| **BigQuery Storage** | <0.5 GB (500 tickers × 3 tablas × 5 años) | **$0** (free tier: 10 GB) |
| **BigQuery Queries** | ~50 MB procesados/día | **$0** (free tier: 1 TB/mes) |
| **Yahoo Finance API** | Free tier (no requiere API key) | **$0** |
| **Google Sheets API** | Lecturas mínimas | **$0** (free tier: 100 requests/100s) |
| **Networking** | Egress negligible | **$0** |

**Total: $0.00/mes** 💚

**Métricas de Diseño:**
- ✅ **Costo Cero**: 100% dentro de los límites del free tier GCP
- ✅ **Escalable**: Maneja 1000+ tickers sin cambios de infraestructura
- ✅ **Baja Latencia**: Procesamiento delta incremental (solo datos nuevos/modificados)
- ✅ **Listo para Producción**: Automatizado, monitoreado, confiable

### Arquitectura

```
Wikipedia (S&P 500) ──┐
                      ├──> Maestro Tickers ──> BigQuery (sp500_tickers)
Google Sheets ────────┘                              │
                                                     │
                                                     ▼
                                          Historico (Verificación Delta)
                                                     │
                                                     ▼
                                          Yahoo Finance (datos 5 años)
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
                                          Notificación Telegram
```

### Hoja de Ruta

Ver [FUTURE.md](./FUTURE.md) para mejoras planificadas:
- **Phase 2**: 6 indicadores técnicos básicos (RSI, SMA, Volumen) - Q3 2026
- **Phase 3**: 9 indicadores avanzados (MACD, Bandas Bollinger, EMA) - Q4 2026
- **Phase 4**: Features ML + señales compuestas - Q1 2027
- **Phase 5**: OpenClaw Skill asistente de inversión - Q2 2027

### Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/darmasatext/sp500-finance-etl
cd sp500-finance-etl

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar pipeline
python src/main.py
```

### Documentación

- [**SETUP.md**](./SETUP.md) - Guía de instalación detallada
- [**ARCHITECTURE.md**](./ARCHITECTURE.md) - Diseño del sistema y flujo del pipeline
- [**FUTURE.md**](./FUTURE.md) - Mejoras futuras
- [**docs/DATA_SCHEMA.md**](./docs/DATA_SCHEMA.md) - Esquemas de tablas BigQuery

### Licencia

Licencia MIT - Copyright (c) 2026 Diego Armas

---

**Author / Autor**: Diego Armas  
**Repository / Repositorio**: https://github.com/darmasatext/sp500-finance-etl
