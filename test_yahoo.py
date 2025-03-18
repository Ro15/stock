import yfinance as yf
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def fetch_historical_data(symbol, period="1mo", interval="1h"):
    """Fetch historical data for a given stock symbol from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            logging.warning(f"⚠️ No data found for {symbol}")
            return None
        return hist
    except Exception as e:
        logging.error(f"⚠️ Error fetching data for {symbol}: {e}")
        return None

def calculate_support_resistance(hist):
    """Calculates basic support and resistance levels using local highs and lows."""
    if hist is None or hist.empty:
        return None, None

    highs = hist["High"]
    lows = hist["Low"]

    # ✅ Define Support as the lowest 5% of price action
    support = np.percentile(lows, 5)
    
    # ✅ Define Resistance as the highest 95% of price action
    resistance = np.percentile(highs, 95)

    return round(support, 2), round(resistance, 2)

if __name__ == "__main__":
    symbol = "AAPL"  # Change symbol to test different stocks
    logging.info(f"📊 Testing Support & Resistance for {symbol}")

    historical_data = fetch_historical_data(symbol, period="1mo", interval="1h")
    
    if historical_data is not None:
        support, resistance = calculate_support_resistance(historical_data)
        logging.info(f"✅ Support for {symbol}: {support}")
        logging.info(f"✅ Resistance for {symbol}: {resistance}")
    else:
        logging.warning("⚠️ Could not calculate support & resistance.")
