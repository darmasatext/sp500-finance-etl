# Changelog | Registro de Cambios

All notable changes to this project will be documented in this file.

Todos los cambios notables a este proyecto serán documentados en este archivo.

---

## [1.0.0] - 2026-03-22

### 🇬🇧 English

#### Added
- Initial release of S&P 500 Finance ETL
- Automated ETL pipeline from Yahoo Finance to BigQuery
- Cloud Run Job deployment
- Telegram notifications with execution metrics
- S&P 500 ticker scraping from Wikipedia
- Personal watchlist integration (Google Sheets)
- Incremental loading strategy:
  - New tickers: Full history from 2020
  - Existing tickers: Only new dates
- Weekend detection (skips execution on Sat/Sun)
- Three BigQuery tables:
  - `sp500_history`: Daily OHLCV data
  - `sp500_tickers`: Master ticker list
  - `sp500_tickers_info`: Fundamental data
- Comprehensive bilingual documentation (EN + ES)
- MIT License
- Production-ready configuration

#### Technical
- Python 3.9
- Google Cloud Run Jobs
- BigQuery append mode
- yfinance for Yahoo Finance API
- gspread for Google Sheets integration
- Error handling and validation
- Environment variables for secrets
- Docker containerization

---

### 🇪🇸 Español

#### Agregado
- Lanzamiento inicial de S&P 500 Finance ETL
- Pipeline ETL automatizado desde Yahoo Finance a BigQuery
- Despliegue en Cloud Run Job
- Notificaciones por Telegram con métricas de ejecución
- Scraping de tickers S&P 500 desde Wikipedia
- Integración con watchlist personal (Google Sheets)
- Estrategia de carga incremental:
  - Tickers nuevos: Historial completo desde 2020
  - Tickers existentes: Solo fechas nuevas
- Detección de fin de semana (omite ejecución Sáb/Dom)
- Tres tablas BigQuery:
  - `sp500_history`: Datos OHLCV diarios
  - `sp500_tickers`: Lista maestra de tickers
  - `sp500_tickers_info`: Datos fundamentales
- Documentación bilingüe completa (EN + ES)
- Licencia MIT
- Configuración lista para producción

#### Técnico
- Python 3.9
- Google Cloud Run Jobs
- Modo append BigQuery
- yfinance para API de Yahoo Finance
- gspread para integración Google Sheets
- Manejo de errores y validación
- Variables de entorno para secretos
- Contenedorización Docker

---

## Future Releases | Lanzamientos Futuros

### [2.0.0] - Planned | Planeado

🇬🇧 **Technical Indicators Addition:**
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands (Upper, Middle, Lower)
- Moving Averages (SMA 20/50/200, EMA 12/26)
- ATR (Average True Range)
- Stochastic Oscillator (K, D)
- OBV (On-Balance Volume)

🇪🇸 **Agregado de Indicadores Técnicos:**
- RSI (Índice de Fuerza Relativa)
- MACD (Convergencia/Divergencia de Medias Móviles)
- Bandas de Bollinger (Superior, Media, Inferior)
- Medias Móviles (SMA 20/50/200, EMA 12/26)
- ATR (Rango Verdadero Promedio)
- Oscilador Estocástico (K, D)
- OBV (Volumen en Balance)

**Impact | Impacto:**
- 🇬🇧 +16 new columns in `sp500_history` table
- 🇪🇸 +16 nuevas columnas en tabla `sp500_history`

---

**Legend | Leyenda:**
- 🇬🇧 Added = New feature | 🇪🇸 Agregado = Nueva funcionalidad
- 🇬🇧 Changed = Modification | 🇪🇸 Cambiado = Modificación
- 🇬🇧 Fixed = Bug fix | 🇪🇸 Arreglado = Corrección de error
- 🇬🇧 Removed = Deletion | 🇪🇸 Eliminado = Eliminación
