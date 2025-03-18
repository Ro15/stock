import logging
from indicators import (
    get_multi_timeframe_analysis, 
    detect_trend_condition, 
    estimate_win_probability, 
    calculate_support_resistance
)
from alerts import send_trade_alert

def analyze_stock(stock):
    """Analyzes stock data, determines trade conditions, and sends alerts if criteria are met."""
    logging.info(f"📊 Fetching data for {stock['symbol']}...")

    # ✅ **Fetch Multi-Timeframe Analysis Data**
    data = get_multi_timeframe_analysis(stock)
    if not data:
        logging.warning(f"⚠️ Skipping {stock['symbol']} due to missing data")
        return

    # ✅ **Extract Technical Indicators (5-Min Timeframe)**
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

    # ✅ **Detect Trend Condition**
    trend_condition, trend_strength = detect_trend_condition(adx_5m, ema50_5m, close_price)

    # ✅ **Estimate Win Probability**
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

    # ✅ **Check for Trade Setup Conditions**
    if (
        adx_5m >= stock["adx_threshold"] and
        ((rsi_5m >= stock["rsi_overbought"] and macd_5m > macd_signal_5m) or
         (rsi_5m <= stock["rsi_oversold"] and macd_5m < macd_signal_5m))
    ):
        trade_type = "CALL" if rsi_5m >= stock["rsi_overbought"] else "PUT"
        
        # ✅ **Send Trade Alert**
        send_trade_alert(
            stock, trade_type, close_price, support_5m, resistance_5m, 
            rsi_5m, macd_5m, macd_signal_5m, adx_5m, atr_5m, volume, trend_condition, win_prob
        )

    # ✅ **Near-Setup Alerts (If Close to Trade Condition)**
    elif (
        adx_5m >= stock["adx_threshold"] - 2 and  # ✅ **Within 2 points of ADX threshold**
        ((rsi_5m >= stock["rsi_overbought"] - 2 and macd_5m > macd_signal_5m) or
         (rsi_5m <= stock["rsi_oversold"] + 2 and macd_5m < macd_signal_5m))
    ):
        logging.warning(f"⚠️ Near Setup Alert for {stock['symbol']} - Monitoring for Confirmation")

        # ✅ **Send Near Setup Alert**
        send_trade_alert(
            stock, 
            "NEAR SETUP ALERT!",  # Mark as Near Setup
            close_price, 
            support_5m, 
            resistance_5m, 
            rsi_5m, 
            macd_5m, 
            macd_signal_5m, 
            adx_5m, 
            atr_5m, 
            volume, 
            trend_condition, 
            win_prob
        )
