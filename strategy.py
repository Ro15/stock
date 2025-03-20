import logging
from indicators import get_multi_timeframe_analysis, detect_trend_condition, estimate_win_probability
from alerts import send_trade_alert

def analyze_stock(stock):
    logging.info(f"📊 Fetching data for {stock['symbol']}...")

    data = get_multi_timeframe_analysis(stock)
    if not data:
        logging.warning(f"⚠️ Skipping {stock['symbol']} due to missing data")
        return

    # Extract indicators
    close_price = data["5m"].get("Close")
    rsi_5m = data["5m"].get("RSI")
    macd_5m = data["5m"].get("MACD")
    macd_signal_5m = data["5m"].get("MACD_signal")
    adx_5m = data["5m"].get("ADX")
    volume = data["5m"].get("Volume", 0)

    # ✅ **Fix Handling of `detect_trend_condition()`**
    trend_condition, trend_strength = detect_trend_condition(adx_5m, close_price)

    # ✅ **Pass Both Values Correctly**
    win_prob = estimate_win_probability(rsi_5m, macd_5m, macd_signal_5m, adx_5m, trend_condition, trend_strength)

    # ✅ **Ensure All Data Is Logged**
    logging.info(f"""📊 Indicators for {stock['symbol']}:
        - Close Price: {close_price}
        - RSI: {rsi_5m} (Overbought: {stock["rsi_overbought"]} / Oversold: {stock["rsi_oversold"]})
        - MACD: {macd_5m} | MACD Signal: {macd_signal_5m}
        - ADX: {adx_5m} (Threshold: {stock["adx_threshold"]})
        - Volume: {volume} (Threshold: {stock["volume_threshold"]})
        - Trend Condition: {trend_condition}
        - Trend Strength: {trend_strength}
        - Win Probability: {win_prob}%
    """)

    # ✅ **Check Trade Conditions**
    is_trade_setup = (
        adx_5m >= stock["adx_threshold"] and
        ((rsi_5m >= stock["rsi_overbought"] and macd_5m > macd_signal_5m) or
         (rsi_5m <= stock["rsi_oversold"] and macd_5m < macd_signal_5m))
    )

    if is_trade_setup:
        trade_type = "CALL" if rsi_5m >= stock["rsi_overbought"] else "PUT"
        send_trade_alert(stock, trade_type, close_price, rsi_5m, macd_5m, macd_signal_5m, adx_5m, volume, trend_condition, win_prob)


def adjust_strategy_based_on_market(market_condition, stock):
    """ Adjusts trading strategy dynamically based on market condition. """
    
    strategies = {
        "Trending": {
            "RSI_Overbought": 75,
            "RSI_Oversold": 25,
            "ADX_Threshold": 30,
            "MACD_Strength": "Strong",
            "Support_Resistance_Check": True
        },
        "Ranging": {
            "RSI_Overbought": 70,
            "RSI_Oversold": 30,
            "ADX_Threshold": 20,
            "MACD_Strength": "Weak",
            "Support_Resistance_Check": False
        },
        "Neutral": {
            "RSI_Overbought": 72,
            "RSI_Oversold": 28,
            "ADX_Threshold": 25,
            "MACD_Strength": "Moderate",
            "Support_Resistance_Check": True
        }
    }

    return strategies.get(market_condition, strategies["Neutral"])  # Default to Neutral if unknown
