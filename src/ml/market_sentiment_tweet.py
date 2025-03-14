import os
from datetime import datetime
import requests
from .sentiment_analyzer import MarketSentimentAnalyzer
from src.config.logger import setup_logging

# Set up logging
logger = setup_logging("MarketSentimentTweet")

def get_market_news():
    """
    Get the latest market news from a financial news API
    
    Returns:
        list: List of news headlines and summaries
    """
    # In a real implementation, this would call an actual financial news API
    # For demonstration purposes, we'll return some sample news
    
    # Sample news data
    sample_news = [
        {
            "headline": "S&P 500 reaches new all-time high as tech stocks surge",
            "summary": "The S&P 500 index reached a new record high today, led by strong performance in technology stocks. Investors are optimistic about upcoming earnings reports.",
            "source": "Market News",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "headline": "Fed signals potential rate cut in upcoming meeting",
            "summary": "Federal Reserve officials hinted at a possible interest rate cut in their next meeting, citing improving inflation data and steady economic growth.",
            "source": "Economic Times",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "headline": "Oil prices drop amid concerns over global demand",
            "summary": "Crude oil prices fell by 3% today as investors worry about weakening global demand and increasing supply from major producers.",
            "source": "Energy News",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    # In a real implementation, you would fetch news from an API
    # Example:
    # response = requests.get("https://financial-news-api.example.com/latest", headers={"Authorization": f"Bearer {API_KEY}"})
    # if response.status_code == 200:
    #     return response.json()["news"]
    # else:
    #     logger.error(f"Failed to fetch news: {response.status_code}")
    #     return []
    
    return sample_news

def format_market_sentiment_tweet(news_item, sentiment_analysis):
    """
    Format a tweet with market news and sentiment analysis
    
    Args:
        news_item (dict): News item with headline and summary
        sentiment_analysis (dict): Sentiment analysis results
        
    Returns:
        str: Formatted tweet text
    """
    # Get sentiment and market impact
    sentiment = sentiment_analysis["sentiment"]["sentiment"]
    market_impact = sentiment_analysis["market_impact"]
    
    # Emoji based on sentiment
    sentiment_emoji = "🟢" if sentiment == "positive" else "🔴" if sentiment == "negative" else "⚪"
    
    # Format the tweet
    tweet = f"""📊 Market AI Analysis:

{sentiment_emoji} {news_item['headline']}

AI Sentiment: {sentiment.capitalize()}
Market Signal: {market_impact}

Source: {news_item['source']}
Time: {news_item['timestamp']}

#MarketAI #FinancialAnalysis #ML"""
    
    return tweet

def generate_market_sentiment_tweets():
    """
    Generate tweets with market news and sentiment analysis
    
    Returns:
        list: List of formatted tweets
    """
    # Get market news
    news_items = get_market_news()
    
    # Get absolute paths to model files
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    model_path = os.path.join(project_root, 'models', 'market_sentiment_model.pkl')
    vectorizer_path = os.path.join(project_root, 'models', 'market_sentiment_vectorizer.pkl')
    
    # Check if model files exist
    model_exists = os.path.exists(model_path)
    vectorizer_exists = os.path.exists(vectorizer_path)
    
    if not model_exists or not vectorizer_exists:
        logger.warning(f"Model files not found. Using rule-based fallback. Model path: {model_path}")
    
    # Load the sentiment analyzer
    analyzer = MarketSentimentAnalyzer(
        model_path=model_path if model_exists else None,
        vectorizer_path=vectorizer_path if vectorizer_exists else None
    )
    
    # Generate tweets
    tweets = []
    for news_item in news_items:
        # Analyze sentiment of the news summary
        sentiment_analysis = analyzer.analyze_market_text(news_item["summary"])
        
        # Format tweet
        tweet = format_market_sentiment_tweet(news_item, sentiment_analysis)
        tweets.append(tweet)
    
    return tweets

# Example function to be called from main.py
def get_market_sentiment_tweet():
    """
    Get a single market sentiment tweet
    
    Returns:
        str: Formatted tweet text
    """
    tweets = generate_market_sentiment_tweets()
    return tweets[0] if tweets else None 