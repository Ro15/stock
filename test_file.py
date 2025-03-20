import logging
from indicators import get_multi_timeframe_analysis, detect_trend_condition, estimate_win_probability
from strategy import analyze_stock
from config import STOCKS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("🔍 Running Full Strategy Test...")

for stock in STOCKS:
    analyze_stock(stock)
