import yfinance as yf
import requests
import pandas as pd
from nsepython import *
import ta

# --- Fetch Equity or Commodity Data from Yahoo Finance ---
def fetch_equity_data(ticker):
    df = yf.download(ticker, period="1mo", interval="1d")
    df['MACD'] = ta.trend.macd(df['Close'])
    df['MACD_signal'] = ta.trend.macd_signal(df['Close'])
    df['RSI'] = ta.momentum.rsi(df['Close'])
    df['VWAP'] = (df['Volume'] * df['Close']).cumsum() / df['Volume'].cumsum()
    bb = ta.volatility.BollingerBands(df['Close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    return df

# --- Fetch Crypto Data from Binance ---
def fetch_crypto_data(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=30"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=["Time", "Open", "High", "Low", "Close", "Volume", "_", "_", "_", "_", "_", "_"])
    df['Close'] = df['Close'].astype(float)
    df['Volume'] = df['Volume'].astype(float)
    df['MACD'] = ta.trend.macd(df['Close'])
    df['MACD_signal'] = ta.trend.macd_signal(df['Close'])
    df['RSI'] = ta.momentum.rsi(df['Close'])
    bb = ta.volatility.BollingerBands(df['Close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['VWAP'] = (df['Volume'] * df['Close']).cumsum() / df['Volume'].cumsum()
    return df

# --- Fetch Option Chain Data from NSE ---
def fetch_option_data(symbol, strike):
    data = nse_optionchain_scrapper(symbol, "index")
    df = pd.DataFrame(data['records']['data'])
    ce = next(item for item in df if item['strikePrice'] == strike)
    return ce['CE']['lastPrice'], ce['CE']['openInterest']

# --- Fetch India VIX (Volatility Index) ---
def fetch_vix():
    vix_data = nsefetch("https://www.nseindia.com/api/quote-equity?symbol=INDIAVIX")
    return float(vix_data['priceInfo']['lastPrice'])

# --- Fetch Put/Call Ratio (PCR) – Placeholder ---
def fetch_pcr(symbol="BANKNIFTY"):
    # Replace with actual API or scraping logic if needed
    return 1.35  # Bullish sentiment
