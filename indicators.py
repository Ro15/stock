import logging
import yfinance as yf
import numpy as np
from tradingview_ta import TA_Handler, Interval

def get_multi_timeframe_analysis(stock):
    """ Fetches technical indicators from TradingView for multiple timeframes and calculates missing ATR using Yahoo Finance. """
    try:
        logging.info(f"Fetching TradingView data for {stock['symbol']}...")

        timeframes = {
            "1m": Interval.INTERVAL_1_MINUTE,
            "5m": Interval.INTERVAL_5_MINUTES,
            "15m": Interval.INTERVAL_15_MINUTES
        }

        analysis_data = {}

        for tf, interval in timeframes.items():
            stock_data = TA_Handler(
                symbol=stock["symbol"],
                screener="america",
                exchange=stock["exchange"],
                interval=interval
            )
            analysis = stock_data.get_analysis()
            analysis_data[tf] = {
                "Close": analysis.indicators.get("close"),
                "RSI": analysis.indicators.get("RSI"),
                "MACD": analysis.indicators.get("MACD.macd"),
                "MACD_signal": analysis.indicators.get("MACD.signal"),
                "ADX": analysis.indicators.get("ADX"),
                "ATR": analysis.indicators.get("ATR"),  # May be missing
                "EMA50": analysis.indicators.get("EMA50"),
            }

        # ✅ Fetch volume from Yahoo Finance
        ticker = yf.Ticker(stock["symbol"])
        hist = ticker.history(period="7d", interval="5m")  # Get 7-day historical data

        volume = hist["Volume"].iloc[-1] if not hist.empty else None
        analysis_data["5m"]["Volume"] = volume
        logging.info(f"📊 Volume for {stock['symbol']}: {volume}")

        # ✅ Fetch Support & Resistance (Only from 5m timeframe)
        sr_levels = get_support_resistance_multi_tf(stock)
        analysis_data["5m"]["Support"] = sr_levels.get("5m", {}).get("Support", "No Data")
        analysis_data["5m"]["Resistance"] = sr_levels.get("5m", {}).get("Resistance", "No Data")

        # ✅ Calculate ATR manually if missing
        if "ATR" not in analysis_data["5m"] or analysis_data["5m"]["ATR"] is None:
            analysis_data["5m"]["ATR"] = calculate_atr(hist)

        return analysis_data

    except Exception as e:
        logging.error(f"⚠️ Error fetching TradingView data for {stock['symbol']}: {e}")
        return {}


def get_support_resistance_multi_tf(stock):
    """ Fetches Support & Resistance from the 5m timeframe using Yahoo Finance """
    try:
        ticker = yf.Ticker(stock["symbol"])
        hist = ticker.history(period="7d", interval="5m")  # Fetch 5m data only

        if hist.empty:
            return {"5m": {"Support": "No Data", "Resistance": "No Data"}}

        # Calculate Support & Resistance based on rolling window
        pivot_low = hist["Low"].rolling(window=10).min()
        pivot_high = hist["High"].rolling(window=10).max()

        support = pivot_low.iloc[-1]
        resistance = pivot_high.iloc[-1]

        return {
            "5m": {
                "Support": round(support, 2) if not np.isnan(support) else "No Data",
                "Resistance": round(resistance, 2) if not np.isnan(resistance) else "No Data"
            }
        }

    except Exception as e:
        logging.error(f"⚠️ Error fetching Support/Resistance for {stock['symbol']}: {e}")
        return {"5m": {"Support": "No Data", "Resistance": "No Data"}}

def calculate_atr(hist, period=14):
    """ Manually calculates ATR using Yahoo Finance data. """
    if hist.empty or len(hist) < period:
        return None

    high_low = hist["High"] - hist["Low"]
    high_close = abs(hist["High"] - hist["Close"].shift())
    low_close = abs(hist["Low"] - hist["Close"].shift())

    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    atr = true_range.rolling(period).mean().iloc[-1]

    return round(atr, 2) if not np.isnan(atr) else None

def estimate_win_probability(rsi, macd, macd_signal, adx, trend_condition, trend_strength):
    """
    Estimate the probability of a successful trade based on indicators.
    """
    macd = float(macd) if isinstance(macd, (int, float)) else 0.0
    macd_signal = float(macd_signal) if isinstance(macd_signal, (int, float)) else 0.0
    adx = float(adx) if isinstance(adx, (int, float)) else 0.0
    rsi = float(rsi) if isinstance(rsi, (int, float)) else 0.0

    win_prob = 50  # Default probability

    if adx > 25:
        win_prob += 10
    if adx > 40:
        win_prob += 10

    if macd > macd_signal:
        win_prob += 10

    if 40 <= rsi <= 60:
        win_prob += 5  # Neutral
    elif rsi > 70 or rsi < 30:
        win_prob += 10  # Strong trend

    if trend_condition == "Trending 🔥":
        win_prob += 10
    elif trend_condition == "Neutral":
        win_prob -= 5

    return min(win_prob, 100)  # ✅ Ensure the probability does not exceed 100%

def detect_trend_condition(adx, ema50, close_price):
    """ Determines if the stock is Trending or Ranging based on ADX and EMAs. """
    if adx is None or close_price is None or ema50 is None:
        return "Neutral", "N/A"  # ✅ Ensure Two Return Values

    if adx > 25 and close_price > ema50:
        return "Trending 🔥", "Strong"
    elif adx < 20:
        return "Ranging ⚖️", "Weak"
    else:
        return "Neutral", "Moderate"
    
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

def calculate_support_resistance(symbol):
    """Calculates support & resistance levels for a stock using historical data."""
    hist = fetch_historical_data(symbol)
    if hist is None or hist.empty:
        return None, None

    highs = hist["High"]
    lows = hist["Low"]

    # ✅ Define Support as the lowest 5% of price action
    support = np.percentile(lows, 5)
    
    # ✅ Define Resistance as the highest 95% of price action
    resistance = np.percentile(highs, 95)

    return round(support, 2), round(resistance, 2)
