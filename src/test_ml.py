import os
from src.ml.sentiment_analyzer import MarketSentimentAnalyzer
from src.ml.market_sentiment_tweet import get_market_sentiment_tweet, get_market_news
from src.config.logger import setup_logging

logging = setup_logging("TestML")

def test_sentiment_analyzer():
    """
    Test the sentiment analyzer with some example texts
    """
    logging.info("Testing sentiment analyzer...")
    
    # Get absolute paths to model files
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    model_path = os.path.join(project_root, 'models', 'market_sentiment_model.pkl')
    vectorizer_path = os.path.join(project_root, 'models', 'market_sentiment_vectorizer.pkl')
    
    analyzer = MarketSentimentAnalyzer(
        model_path=model_path if os.path.exists(model_path) else None,
        vectorizer_path=vectorizer_path if os.path.exists(vectorizer_path) else None
    )
    
    texts = [
        "The market is showing strong growth with increasing volume",
        "Stocks plummeted today as investors reacted to disappointing earnings",
        "Trading remained flat with mixed signals from economic indicators"
    ]
    
    for text in texts:
        result = analyzer.analyze_market_text(text)
        logging.info(f"Text: {text}")
        logging.info(f"Sentiment: {result['sentiment']['sentiment']}")
        logging.info(f"Market Impact: {result['market_impact']}")
        logging.info("-" * 50)

def test_market_sentiment_tweet():
    """
    Test generating a market sentiment tweet
    """
    logging.info("Testing market sentiment tweet generation...")
    
    # Get news
    news_items = get_market_news()
    logging.info(f"Retrieved {len(news_items)} news items")
    
    # Get tweet
    tweet = get_market_sentiment_tweet()
    
    if tweet:
        logging.info("Generated tweet:")
        logging.info("-" * 50)
        logging.info(tweet)
        logging.info("-" * 50)
    else:
        logging.error("Failed to generate tweet")

if __name__ == "__main__":
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Test sentiment analyzer
    test_sentiment_analyzer()
    
    # Test tweet generation
    test_market_sentiment_tweet()
    
    logging.info("All tests completed") 