import logging
from indicators import get_multi_timeframe_analysis, detect_trend_condition, estimate_win_probability
from alerts import send_trade_alert
from indicators import calculate_support_resistance

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
    atr_5m = data["5m"].get("ATR", "N/A")
    volume = data["5m"].get("Volume", 0)
    ema50_5m = data["5m"].get("EMA50", "N/A")

    # ✅ **Fetch Support & Resistance**
    support_5m, resistance_5m = calculate_support_resistance(stock["symbol"])

    # ✅ **Fix Handling of `detect_trend_condition()`**
    trend_info = detect_trend_condition(adx_5m, ema50_5m, close_price)

    if isinstance(trend_info, tuple):  # If it returns multiple values
        trend_condition, trend_strength = trend_info
    else:  # If it returns only one value
        trend_condition = trend_info
        trend_strength = "N/A"

    # ✅ **Pass Both Values Correctly**
    win_prob = estimate_win_probability(rsi_5m, macd_5m, macd_signal_5m, adx_5m, trend_condition, trend_strength)

    # ✅ **Ensure All Data Is Logged**
    logging.info(f"""📊 Indicators for {stock['symbol']}:
        - Close Price: {close_price}
        - RSI: {rsi_5m} (Overbought: {stock["rsi_overbought"]} / Oversold: {stock["rsi_oversold"]})
        - MACD: {macd_5m} | MACD Signal: {macd_signal_5m}
        - ADX: {adx_5m} (Threshold: {stock["adx_threshold"]})
        - ATR: {atr_5m}
        - Volume: {volume} (Threshold: {stock["volume_threshold"]})
        - Support: {support_5m} | Resistance: {resistance_5m} ✅ FIXED
        - Trend: {trend_condition} ({trend_strength})
        - Win Probability: {win_prob}%
    """)

    # ✅ **Check Trade Conditions**
    if (
        adx_5m >= stock["adx_threshold"] and
        ((rsi_5m >= stock["rsi_overbought"] and macd_5m > macd_signal_5m) or
         (rsi_5m <= stock["rsi_oversold"] and macd_5m < macd_signal_5m))
    ):
        trade_type = "CALL" if rsi_5m >= stock["rsi_overbought"] else "PUT"
        send_trade_alert(stock, trade_type, close_price, support_5m, resistance_5m, rsi_5m, macd_5m, macd_signal_5m, adx_5m, atr_5m, volume, trend_condition, win_prob)
