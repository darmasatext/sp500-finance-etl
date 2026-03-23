-- S&P 500 Finance ETL - BigQuery Schema
-- Dataset: finance_data
-- Description: S&P 500 stock data (historical prices, tickers info, fundamentals)

-- ======================
-- Table 1: sp500_history
-- ======================
-- Daily stock prices (OHLCV)

CREATE TABLE IF NOT EXISTS `last-240000.finance_data.sp500_history` (
  Date DATE NOT NULL,
  Ticker STRING NOT NULL,
  Price FLOAT64,      -- Adjusted Close Price
  Volume INT64
)
PARTITION BY Date
CLUSTER BY Ticker, Date
OPTIONS(
  description="S&P 500 daily historical stock prices (Adjusted Close + Volume)",
  labels=[("source", "yahoo-finance"), ("version", "v1")]
);

-- Sample query: Last 30 days for specific ticker
-- SELECT Date, Ticker, Price, Volume
-- FROM `last-240000.finance_data.sp500_history`
-- WHERE Ticker = 'AAPL'
--   AND Date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
-- ORDER BY Date DESC;

-- ======================
-- Table 2: sp500_tickers (MAESTRA)
-- ======================
-- Master list of S&P 500 companies

CREATE TABLE IF NOT EXISTS `last-240000.finance_data.sp500_tickers` (
  Ticker STRING NOT NULL,
  Company_Name STRING,
  Sector STRING,
  Industry STRING,
  Date_Added DATE,
  Last_Updated TIMESTAMP
)
CLUSTER BY Ticker
OPTIONS(
  description="Master table of S&P 500 company information",
  labels=[("source", "wikipedia"), ("version", "v1")]
);

-- Sample query: All tech companies
-- SELECT Ticker, Company_Name, Industry
-- FROM `last-240000.finance_data.sp500_tickers`
-- WHERE Sector = 'Information Technology'
-- ORDER BY Company_Name;

-- ======================
-- Table 3: sp500_tickers_info
-- ======================
-- Fundamental data and company profiles

CREATE TABLE IF NOT EXISTS `last-240000.finance_data.sp500_tickers_info` (
  Ticker STRING NOT NULL,
  Market_Cap FLOAT64,
  PE_Ratio FLOAT64,
  Dividend_Yield FLOAT64,
  EPS FLOAT64,           -- Earnings Per Share
  Beta FLOAT64,          -- Volatility vs market
  Week_52_High FLOAT64,
  Week_52_Low FLOAT64,
  Website STRING,
  Description STRING,
  CEO STRING,
  Employees INT64,
  Country STRING,
  Exchange STRING,
  Last_Updated TIMESTAMP
)
CLUSTER BY Ticker
OPTIONS(
  description="Fundamental metrics and company profiles for S&P 500 stocks",
  labels=[("source", "yahoo-finance"), ("version", "v1")]
);

-- Sample query: High dividend stocks
-- SELECT Ticker, Market_Cap, PE_Ratio, Dividend_Yield
-- FROM `last-240000.finance_data.sp500_tickers_info`
-- WHERE Dividend_Yield > 3.0
-- ORDER BY Dividend_Yield DESC
-- LIMIT 20;

-- ======================
-- FUTURE ENHANCEMENTS (v2.0)
-- ======================
-- Planned additional columns for sp500_history:

-- ALTER TABLE `last-240000.finance_data.sp500_history`
-- ADD COLUMN IF NOT EXISTS RSI_14 FLOAT64,           -- Relative Strength Index
-- ADD COLUMN IF NOT EXISTS MACD FLOAT64,             -- Moving Average Convergence Divergence
-- ADD COLUMN IF NOT EXISTS MACD_Signal FLOAT64,
-- ADD COLUMN IF NOT EXISTS MACD_Histogram FLOAT64,
-- ADD COLUMN IF NOT EXISTS BB_Upper FLOAT64,         -- Bollinger Bands Upper
-- ADD COLUMN IF NOT EXISTS BB_Middle FLOAT64,        -- Bollinger Bands Middle
-- ADD COLUMN IF NOT EXISTS BB_Lower FLOAT64,         -- Bollinger Bands Lower
-- ADD COLUMN IF NOT EXISTS SMA_20 FLOAT64,           -- Simple Moving Average 20 days
-- ADD COLUMN IF NOT EXISTS SMA_50 FLOAT64,
-- ADD COLUMN IF NOT EXISTS SMA_200 FLOAT64,
-- ADD COLUMN IF NOT EXISTS EMA_12 FLOAT64,           -- Exponential Moving Average
-- ADD COLUMN IF NOT EXISTS EMA_26 FLOAT64,
-- ADD COLUMN IF NOT EXISTS ATR_14 FLOAT64,           -- Average True Range
-- ADD COLUMN IF NOT EXISTS Stochastic_K FLOAT64,     -- Stochastic Oscillator
-- ADD COLUMN IF NOT EXISTS Stochastic_D FLOAT64,
-- ADD COLUMN IF NOT EXISTS OBV FLOAT64;              -- On-Balance Volume

-- 🇬🇧 Note: These technical indicators will be calculated and added in Phase 2
-- 🇪🇸 Nota: Estos indicadores técnicos se calcularán y agregarán en Fase 2
