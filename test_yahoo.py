import logging
from indicators import calculate_atr_tradingview

# ✅ Configure logging for clear output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ List of stocks to test
TEST_STOCKS = ["AAPL", "TSLA", "NVDA", "AMZN", "MSFT"]

logging.info("🔍 Running ATR Calculation Test...")

for stock in TEST_STOCKS:
    logging.info(f"📊 Testing ATR calculation for {stock}...")
    
    atr_value = calculate_atr_tradingview(stock)

    if atr_value is not None:
        logging.info(f"✅ ATR for {stock}: {atr_value}")
    else:
        logging.warning(f"⚠️ ATR for {stock} is N/A. Check market hours or TradingView data.")

logging.info("✅ ATR Test Completed!")
