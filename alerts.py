import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message, bot_type="primary"):
    """
    Sends a Telegram alert using the specified bot (primary/secondary).
    
    Args:
        message (str): The message to send.
        bot_type (str): Which bot to use ('primary' or 'secondary').
    """
    bot_token = TELEGRAM_BOT_TOKEN.get(bot_type)
    chat_id = TELEGRAM_CHAT_ID.get(bot_type)

    if not bot_token or not chat_id:
        logging.error(f"⚠️ Invalid bot type: {bot_type}")
        return

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            logging.info(f"📩 Telegram Alert Sent Successfully via {bot_type.capitalize()} Bot")
        else:
            logging.error(f"⚠️ Failed to send alert via {bot_type.capitalize()} Bot: {response.json()}")
    except Exception as e:
        logging.error(f"⚠️ Error sending Telegram alert: {e}")

def send_trade_alert(stock, trade_type, close_price, support, resistance, rsi, macd, macd_signal, adx, atr, volume, trend, win_prob):
    """
    Sends a trade alert message for a given stock.
    """
    message = f"""
🚀 *Trade Alert for {stock['symbol']}* 🚀
🔹 *Trade Type:* {trade_type.upper()}
📈 *Close Price:* ${close_price:.2f}
📊 *Support:* ${support} | *Resistance:* ${resistance}

📊 *Indicators:*
    - RSI: {rsi:.2f} (Overbought: {stock['rsi_overbought']} / Oversold: {stock['rsi_oversold']})
    - MACD: {macd:.5f} | MACD Signal: {macd_signal:.5f}
    - ADX: {adx:.2f} (Threshold: {stock['adx_threshold']})
    - ATR: {atr}
    - Volume: {volume:,} (Threshold: {stock['volume_threshold']})
    - Trend: {trend}
    - *Win Probability:* {win_prob}%

📩 *Sent via Trading Bot*
    """

    # ✅ Send Alert to Both Primary and Secondary Bots
    send_telegram_alert(message, bot_type="primary")
    send_telegram_alert(message, bot_type="secondary")
