import logging
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_trade_alert(stock, trade_type, close_price, support, resistance, rsi, macd, macd_signal, adx, atr, volume, trend, win_prob, is_near_setup=False):
    """ Sends a trade alert or near setup alert to both primary & secondary Telegram IDs """

    alert_type = "⚠️ Near Setup Alert!" if is_near_setup else "🚀 Trade Alert"
    alert_message = "Monitoring for Confirmation 📉📈" if is_near_setup else "Confirmed Trade Signal ✅"

    message = f"""
{alert_type} for {stock['symbol']} 🚀
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

📢 {alert_message}
    """

    send_telegram_alert(message)

def send_telegram_alert(message):
    """ Sends alert to both primary and secondary Telegram chat IDs """

    def send_request(bot_token, chat_id):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        return requests.post(url, json=payload)

    # Send to both primary and secondary Telegram chat IDs
    for bot_token, chat_id in [
        (TELEGRAM_BOT_TOKEN['primary'], TELEGRAM_CHAT_ID['primary']),
        (TELEGRAM_BOT_TOKEN['secondary'], TELEGRAM_CHAT_ID['secondary'])
    ]:
        response = send_request(bot_token, chat_id)
        
        if response.status_code == 200:
            logging.info(f"📩 Telegram Alert Sent Successfully to Chat ID {chat_id} ✅")
        else:
            logging.error(f"⚠️ Failed to send alert to Chat ID {chat_id}: {response.text}")
