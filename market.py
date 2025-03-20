import logging
from tradingview_ta import TA_Handler, Interval

def get_market_condition():
    """ Analyze overall market condition to adjust trading strategy. """
    try:
        logging.info("📊 Fetching Market Data from TradingView...")

        spy_data = TA_Handler(
            symbol="SPY",
            screener="america",
            exchange="AMEX",
            interval=Interval.INTERVAL_1_HOUR
        )
        analysis = spy_data.get_analysis()

        # ✅ Extract only required indicators (Removing ATR & Support/Resistance)
        adx = analysis.indicators.get("ADX")
        rsi = analysis.indicators.get("RSI")
        macd = analysis.indicators.get("MACD.macd")
        macd_signal = analysis.indicators.get("MACD.signal")

        if adx is None or rsi is None or macd is None or macd_signal is None:
            raise ValueError("⚠️ Missing key market indicators from TradingView.")

        logging.info(f"📊 Market ADX: {adx}, RSI: {rsi}, MACD: {macd}, MACD Signal: {macd_signal}")

        # ✅ Determine Market Condition Based on ADX, RSI, and MACD
        if adx > 25 and macd > macd_signal:
            return "Trending"
        elif adx < 20 and -60 <= rsi <= 60:
            return "Ranging"
        elif -2 < macd - macd_signal < 2:
            return "Neutral"
        else:
            return "Unknown"

    except Exception as e:
        logging.error(f"⚠️ Error analyzing market: {e}")
        return "Unknown"
