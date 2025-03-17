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
                "ATR": analysis.indicators.get("ATR"),
                "EMA50": analysis.indicators.get("EMA50"),
                "Support": analysis.indicators.get("Pivot.M.S3"),  # Support Level
                "Resistance": analysis.indicators.get("Pivot.M.R3")  # Resistance Level
            }

        # ✅ Fetch volume from Yahoo Finance
        ticker = yf.Ticker(stock["symbol"])
        hist = ticker.history(period="7d", interval="5m")  # Get 7-day historical data

        volume = hist["Volume"].iloc[-1] if not hist.empty else 0
        analysis_data["5m"]["Volume"] = volume
        logging.info(f"📊 Volume for {stock['symbol']}: {volume}")

        # ✅ Calculate ATR manually if missing
        if "ATR" not in analysis_data["5m"] or analysis_data["5m"]["ATR"] is None:
            analysis_data["5m"]["ATR"] = calculate_atr(hist)

        return analysis_data

    except Exception as e:
        logging.error(f"⚠️ Error fetching TradingView data for {stock['symbol']}: {e}")
        return {}

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

def detect_trend_condition(adx, ema50, close_price):
    """ Determines if the stock is Trending or Ranging based on ADX and EMAs. """
    if adx is None or close_price is None or ema50 is None:
        return "Neutral", 50  # Default to Neutral if any value is missing

    if adx > 25 and close_price > ema50:
        return "Trending 🔥", 70
    elif adx < 20:
        return "Ranging ⚖️", 50
    else:
        return "Neutral", 60

def estimate_win_probability(rsi, macd, macd_signal, adx, trend_condition, trend_strength):
    """ Estimate the probability of a successful trade based on indicators. """
    # Ensure values are properly converted to floats
    macd = float(macd) if isinstance(macd, (int, float)) else 0.0
    macd_signal = float(macd_signal) if isinstance(macd_signal, (int, float)) else 0.0
    adx = float(adx) if isinstance(adx, (int, float)) else 0.0
    rsi = float(rsi) if isinstance(rsi, (int, float)) else 0.0

    win_prob = 50

    if adx > 25:
        win_prob += 10
    if adx > 40:
        win_prob += 10

    if macd > macd_signal:
        win_prob += 10

    if 40 <= rsi <= 60:
        win_prob += 5
    elif rsi > 70 or rsi < 30:
        win_prob += 10

    if trend_condition == "Trending 🔥":
        win_prob += 10
    elif trend_condition == "Neutral":
        win_prob -= 5

    return min(win_prob, 100)
