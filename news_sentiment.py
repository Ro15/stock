import logging
from newsapi import NewsApiClient
from textblob import TextBlob

# Your API key from https://newsapi.org/
NEWS_API_KEY = "7c6cd3a6a9af474bb42ce3ad8a85bf04"

def fetch_news(stock_symbol, num_articles=5):
    """
    Fetch recent news headlines related to a given stock.
    If the API limit is reached, it will return an empty list.
    """
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        query = f"{stock_symbol} stock"
        articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='publishedAt',
            page_size=num_articles
        )

        if articles.get("status") == "error":
            logging.warning(f"⚠️ News API Limit Reached - Skipping news for {stock_symbol}")
            return []

        return articles.get("articles", [])

    except Exception as e:
        logging.error(f"⚠️ Error fetching news for {stock_symbol}: {e}")
        return []

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using TextBlob.
    Returns 'Positive', 'Negative', or 'Neutral' sentiment.
    """
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0.2:
        sentiment_label = "Positive"
    elif sentiment_score < -0.2:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return sentiment_label, sentiment_score

def get_stock_news_sentiment(stock_symbol):
    """
    Fetches recent news and analyzes sentiment.
    If news is unavailable due to API limits, it returns 'Neutral'.
    """
    articles = fetch_news(stock_symbol)
    
    if not articles:
        logging.warning(f"⚠️ No recent news found for {stock_symbol} - Skipping sentiment analysis")
        return "Neutral", 0.0  # ✅ Default to Neutral if news is unavailable

    combined_titles = ' '.join(article['title'] for article in articles)
    sentiment_label, sentiment_score = analyze_sentiment(combined_titles)

    logging.info(f"📰 News Sentiment for {stock_symbol}: {sentiment_label} ({sentiment_score:.2f})")

    return sentiment_label, sentiment_score
