# config.py
STOCKS = [
    {"symbol": "AAPL", "exchange": "NASDAQ", "rsi_overbought": 70, "rsi_oversold": 30, "adx_threshold": 25, "volume_threshold": 100000},
    {"symbol": "TSLA", "exchange": "NASDAQ", "rsi_overbought": 75, "rsi_oversold": 25, "adx_threshold": 30, "volume_threshold": 200000},
    {"symbol": "NVDA", "exchange": "NASDAQ", "rsi_overbought": 72, "rsi_oversold": 28, "adx_threshold": 28, "volume_threshold": 150000},
    {"symbol": "AMZN", "exchange": "NASDAQ", "rsi_overbought": 68, "rsi_oversold": 32, "adx_threshold": 22, "volume_threshold": 180000},
    {"symbol": "META", "exchange": "NASDAQ", "rsi_overbought": 73, "rsi_oversold": 27, "adx_threshold": 29, "volume_threshold": 160000},
    {"symbol": "GOOGL", "exchange": "NASDAQ", "rsi_overbought": 71, "rsi_oversold": 29, "adx_threshold": 27, "volume_threshold": 140000},
    {"symbol": "AMD", "exchange": "NASDAQ", "rsi_overbought": 74, "rsi_oversold": 26, "adx_threshold": 30, "volume_threshold": 120000},
    {"symbol": "BABA", "exchange": "NYSE", "rsi_overbought": 69, "rsi_oversold": 31, "adx_threshold": 25, "volume_threshold": 130000},
    {"symbol": "COIN", "exchange": "NASDAQ", "rsi_overbought": 72, "rsi_oversold": 28, "adx_threshold": 28, "volume_threshold": 100000},
    {"symbol": "MSFT", "exchange": "NASDAQ", "rsi_overbought": 70, "rsi_oversold": 30, "adx_threshold": 26, "volume_threshold": 190000},
]

TELEGRAM_BOT_TOKEN = {"primary":"7996722753:AAF2wJHA2AxWxg3AHYRTgUpPsMkmxrSitnI",
                      "secondary":"7343346012:AAFiMGtLYFyV07-e9CfEPqeDzGVSArd7jaY"}

TELEGRAM_CHAT_ID = {"primary":"5620276632",
                    "secondary":"5662316389"}
