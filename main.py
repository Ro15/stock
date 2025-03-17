import time
import logging
from config import STOCKS
from strategy import analyze_stock

# ✅ Configure logging to log both to a file and to the terminal (without emojis)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("trade_alerts.log", encoding="utf-8"),  # Saves logs to file
        logging.StreamHandler()  # Logs to terminal
    ]
)

while True:
    for stock in STOCKS:
        analyze_stock(stock)
    logging.info("Waiting for the next cycle...")
    time.sleep(180)  # Runs every 5 minutes
