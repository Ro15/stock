import logging
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_trade_alert(stock, trade_type, close_price, support, resistance, rsi, macd, macd_signal, adx, atr, volume, trend, win_prob):
    message = f"""
🚀 Trade Alert for {stock['symbol']} 🚀
🔹 Trade Type: {trade_type}
📈 Close Price: ${close_price}
📊 Support: ${support} | Resistance: ${resistance} ✅ FIXED

📊 Indicators:
    - RSI: {rsi} (Overbought: {stock['rsi_overbought']} / Oversold: {stock['rsi_oversold']})
    - MACD: {macd} | MACD Signal: {macd_signal}
    - ADX: {adx} (Threshold: {stock["adx_threshold"]})
    - ATR: {atr}
    - Volume: {volume} (Threshold: {stock["volume_threshold"]})
    - Trend: {trend}
    - Win Probability: {win_prob}%
    """

    send_telegram_alert(message)

def send_telegram_alert(message):
    """ Sends alert to Telegram """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN['primary']}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID["primary"],
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        logging.info("📩 Telegram Alert Sent Successfully")
    else:
        logging.error(f"⚠️ Failed to send alert: {response.text}")
