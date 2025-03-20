import logging
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_trade_alert(stock, trade_type, close_price, rsi, macd, macd_signal, adx, volume, trend, win_prob):
    """ Sends a trade alert to both primary & secondary Telegram IDs """

    message = f"""
🚀 Trade Alert for {stock['symbol']} 🚀
🔹 Trade Type: {trade_type}
📈 Close Price: ${close_price}

📊 Indicators:
    - RSI: {rsi} (Overbought: {stock['rsi_overbought']} / Oversold: {stock['rsi_oversold']})
    - MACD: {macd} | MACD Signal: {macd_signal}
    - ADX: {adx} (Threshold: {stock["adx_threshold"]})
    - Volume: {volume} (Threshold: {stock["volume_threshold"]})
    - Trend Condition: {trend}
    - Win Probability: {win_prob}%
    """

    send_telegram_alert(message)

def send_telegram_alert(message):
    """ Sends alert to both primary and secondary Telegram chat IDs """
    for bot_token, chat_id in [
        (TELEGRAM_BOT_TOKEN['primary'], TELEGRAM_CHAT_ID['primary']),
        (TELEGRAM_BOT_TOKEN['secondary'], TELEGRAM_CHAT_ID['secondary'])
    ]:
        response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})

        if response.status_code == 200:
            logging.info(f"📩 Telegram Alert Sent Successfully to Chat ID {chat_id} ✅")
        else:
            logging.error(f"⚠️ Failed to send alert to Chat ID {chat_id}: {response.text}")
