import logging
from indicators import get_multi_timeframe_analysis

# ✅ Enable logging to see output in terminal
logging.basicConfig(level=logging.INFO)

def test_support_resistance():
    test_stock = {
        "symbol": "AAPL",
        "exchange": "NASDAQ"
    }

    logging.info(f"🔍 Testing Support & Resistance for {test_stock['symbol']}...")

    # Fetch market data
    data = get_multi_timeframe_analysis(test_stock)

    if not data:
        logging.error(f"❌ Failed to retrieve data for {test_stock['symbol']}")
        return

    # Extract support & resistance
    support_5m = data["5m"].get("Support", "N/A")
    resistance_5m = data["5m"].get("Resistance", "N/A")

    # ✅ Print Results
    logging.info(f"📊 Support Level: {support_5m}")
    logging.info(f"📊 Resistance Level: {resistance_5m}")

# Run the test
test_support_resistance()
