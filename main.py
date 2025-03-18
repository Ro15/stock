import time
import logging
from config import STOCKS
from strategy import analyze_stock

# ✅ Configure logging (UTF-8 support for emojis, log rotation for long-running scripts)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("trade_alerts.log", encoding="utf-8"),  # Logs to file
        logging.StreamHandler()  # Logs to terminal
    ]
)

logging.info("🚀 Trading Bot Started!")

while True:
    try:
        for stock in STOCKS:
            try:
                analyze_stock(stock)
            except Exception as e:
                logging.error(f"⚠️ Error analyzing {stock['symbol']}: {e}")

        logging.info("⏳ Waiting for the next cycle...")
        time.sleep(180)  # ✅ Waits 3 minutes before the next cycle

    except KeyboardInterrupt:
        logging.info("🛑 Trading Bot Stopped by User")
        break  # ✅ Stops execution safely on manual interruption
