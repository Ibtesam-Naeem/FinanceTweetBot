import os
from src.ml.sentiment_analyzer import MarketSentimentAnalyzer
from src.config.logger import setup_logging

logging = setup_logging("Train Model")

def train_sentiment_model():
    """
    Train the market sentiment analysis model with sample data
    """
    # Creates directories for model and tokenizer if they don't exist
    os.makedirs('models', exist_ok=True)
    
    # Sample training data
    # Format: (text, label) where label is 0=negative, 1=neutral, 2=positive
    training_data = [
        # Negative examples
        ("Stocks plummeted as investors reacted to disappointing earnings", 0),
        ("The market crashed following the Fed's announcement", 0),
        ("Bearish sentiment dominates as economic indicators show weakness", 0),
        ("Investors are selling off shares amid growing concerns", 0),
        ("The index fell sharply, erasing all gains from the previous month", 0),
        ("Disappointing jobs report sends markets tumbling", 0),
        ("Recession fears trigger massive sell-off", 0),
        ("Company shares drop 15% after missing revenue targets", 0),
        ("Market volatility increases as uncertainty grows", 0),
        ("Downward pressure continues as trading volume decreases", 0),
        
        # Neutral examples
        ("Markets closed mixed with no clear direction", 1),
        ("Investors remain cautious as they await economic data", 1),
        ("Trading volume was average with balanced buying and selling", 1),
        ("The index fluctuated throughout the day, ending flat", 1),
        ("Analysts have mixed opinions on the market's next move", 1),
        ("Sideways trading pattern continues for the third consecutive day", 1),
        ("Company earnings met expectations with no surprises", 1),
        ("Fed maintains current policy with no changes announced", 1),
        ("Market participants are waiting for more clarity", 1),
        ("Neither bulls nor bears gained control in today's session", 1),
        
        # Positive examples
        ("Stocks rallied on strong economic data and positive earnings", 2),
        ("The market surged to new all-time highs on heavy volume", 2),
        ("Bullish momentum continues as investors pile into equities", 2),
        ("Company shares jumped 10% after beating earnings expectations", 2),
        ("The index posted its best day in months as sentiment improved", 2),
        ("Strong jobs report fuels market rally", 2),
        ("Investors are optimistic about future growth prospects", 2),
        ("Upward trend remains intact as buyers dominate the market", 2),
        ("Tech stocks lead the market higher on positive news", 2),
        ("Market breadth improves as more stocks participate in the rally", 2)
    ]
    
    # Split into texts and labels
    texts = [item[0] for item in training_data]
    labels = [item[1] for item in training_data]
    
    # Create and train the model
    analyzer = MarketSentimentAnalyzer()
    
    # Train the model
    results = analyzer.train(
        texts=texts,
        labels=labels,
        test_size=0.2,
        random_state=42
    )
    
    logging.info(f"Model training completed with accuracy: {results['accuracy']:.4f}")
    
    # Saves the model and vectorizer
    analyzer.save_model(
        model_path='models/market_sentiment_model.pkl',
        vectorizer_path='models/market_sentiment_vectorizer.pkl'
    )
    
    return analyzer

if __name__ == "__main__":
    train_sentiment_model() 