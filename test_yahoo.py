import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)

def fetch_volume_debug(stock_symbol):
    """
    Fetches and prints volume data for debugging.
    """
    try:
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period="1d", interval="5m")  # Get today's 5-minute data

        if hist.empty:
            logging.warning(f"⚠️ No volume data found for {stock_symbol}")
            return None

        logging.info(f"🔍 Full Yahoo Finance Data for {stock_symbol}:")
        print(hist.tail(10))  # ✅ Print last 10 rows to debug

        latest_volume = hist["Volume"].iloc[-1] if "Volume" in hist.columns else None

        if latest_volume is None:
            logging.warning(f"⚠️ Volume column missing for {stock_symbol}")
        else:
            logging.info(f"📊 Latest Volume for {stock_symbol}: {latest_volume}")

        return latest_volume

    except Exception as e:
        logging.error(f"❌ Error fetching volume for {stock_symbol}: {e}")
        return None

# 🔹 Test with a stock symbol (e.g., AAPL, TSLA, NVDA)
if __name__ == "__main__":
    stock_symbol = "AAPL" # Change this to test different stocks
    fetch_volume_debug(stock_symbol)
