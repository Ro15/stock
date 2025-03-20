import logging
import numpy as np
from tradingview_ta import TA_Handler, Interval

def get_multi_timeframe_analysis(stock):
    """ Fetches technical indicators from TradingView for multiple timeframes. """
    try:
        logging.info(f"📊 Fetching TradingView data for {stock['symbol']}...")

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
                "Volume": analysis.indicators.get("volume", 0),
            }

        return analysis_data

    except Exception as e:
        logging.error(f"⚠️ Error fetching TradingView data for {stock['symbol']}: {e}")
        return {}

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

def detect_trend_condition(adx, close_price):
    """ Determines if the stock is Trending or Ranging based on ADX. """
    if adx is None or close_price is None:
        return "Neutral", "N/A"

    if adx > 25:
        return "Trending 🔥", "Strong"
    elif adx < 20:
        return "Ranging ⚖️", "Weak"
    else:
        return "Neutral", "Moderate"



def get_market_data():
    """Fetches SPY market data from TradingView for dynamic strategy switching."""
    try:
        logging.info("📊 Fetching Market Data from TradingView...")

        spy_data = TA_Handler(
            symbol="SPY",
            screener="america",
            exchange="AMEX",
            interval=Interval.INTERVAL_1_HOUR
        )
        analysis = spy_data.get_analysis()

        market_data = {
            "Close": analysis.indicators.get("close"),
            "RSI": analysis.indicators.get("RSI"),
            "MACD": analysis.indicators.get("MACD.macd"),
            "MACD_signal": analysis.indicators.get("MACD.signal"),
            "ADX": analysis.indicators.get("ADX"),
        }
        logging.info(f"✅ SPY Data Retrieved Successfully!")
        for key, value in market_data.items():
            logging.info(f"🔹 {key}: {value}")

        return market_data

    except Exception as e:
        logging.error(f"⚠️ Error analyzing market: {e}")
        return {}


