from data_fetcher import fetch_equity_data, fetch_crypto_data, fetch_option_data
import requests, os

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

def send_signal(name, price, strategy, reason, target, sl, confidence):
    msg = f"""
📌 SIGNAL – {name}
🟢 BUY @ ₹{price:.2f}
🎯 Target: {target} | 🛑 SL: {sl}
📈 Confidence: {confidence} ✅ High
📚 Strategy: {strategy}
🧠 Reason: {reason}
"""
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                  data={"chat_id": chat_id, "text": msg})

# --- NIFTY 50 ---
nifty_df = fetch_equity_data("^NSEI")
if nifty_df['MACD'].iloc[-1] > nifty_df['MACD_signal'].iloc[-1] and \
   nifty_df['RSI'].iloc[-1] > 50 and \
   nifty_df['Close'].iloc[-1] > nifty_df['VWAP'].iloc[-1]:
    send_signal("NIFTY 50", nifty_df['Close'].iloc[-1], "VWAP Breakout", "MACD + RSI + VWAP", "+2%", "-1%", "85%")

# --- NIFTY 500 Stocks (Example: RELIANCE) ---
reliance_df = fetch_equity_data("RELIANCE.NS")
if reliance_df['MACD'].iloc[-1] > reliance_df['MACD_signal'].iloc[-1] and \
   reliance_df['RSI'].iloc[-1] > 50 and \
   reliance_df['Close'].iloc[-1] > reliance_df['VWAP'].iloc[-1]:
    send_signal("RELIANCE", reliance_df['Close'].iloc[-1], "Trend Continuation", "MACD + RSI + VWAP", "+3%", "-1.5%", "88%")

# --- Currency Pairs ---
usd_df = fetch_equity_data("USDINR=X")
eur_df = fetch_equity_data("EURINR=X")
for name, df in [("USD/INR", usd_df), ("EUR/INR", eur_df)]:
    if df['MACD'].iloc[-1] > df['MACD_signal'].iloc[-1] and df['RSI'].iloc[-1] > 50:
        send_signal(name, df['Close'].iloc[-1], "Momentum", "MACD + RSI", "+1.5%", "-0.5%", "80%")

# --- Crude Oil ---
oil_df = fetch_equity_data("CL=F")
if oil_df['MACD'].iloc[-1] > oil_df['MACD_signal'].iloc[-1] and \
   oil_df['RSI'].iloc[-1] > 50 and \
   oil_df['Close'].iloc[-1] > oil_df['VWAP'].iloc[-1]:
    send_signal("Crude Oil", oil_df['Close'].iloc[-1], "Volatility Expansion", "MACD + RSI + VWAP", "+4%", "-2%", "87%")
