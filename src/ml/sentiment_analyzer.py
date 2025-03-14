import os
import numpy as np
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from src.config.logger import setup_logging

# Set up logging
logger = setup_logging("SentimentAnalyzer")

class MarketSentimentAnalyzer:
    def __init__(self, model_path=None, vectorizer_path=None):
        """
        Initialize the sentiment analyzer with optional pre-trained model and vectorizer
        
        Args:
            model_path (str, optional): Path to saved model
            vectorizer_path (str, optional): Path to saved vectorizer
        """
        self.model = None
        self.vectorizer = None
        
        # Download NLTK resources if not already downloaded
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        
        # Load pre-trained model and vectorizer if provided
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Loaded model from {model_path}")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
        
        if vectorizer_path and os.path.exists(vectorizer_path):
            try:
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                logger.info(f"Loaded vectorizer from {vectorizer_path}")
            except Exception as e:
                logger.error(f"Error loading vectorizer: {e}")
    
    def preprocess_text(self, text):
        """
        Preprocess text for sentiment analysis
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Simple tokenization to avoid punkt_tab issue
        tokens = text.split()
        
        # Remove stopwords
        tokens = [word for word in tokens if word not in self.stop_words]
        
        # Join tokens back into string
        return ' '.join(tokens)
    
    def build_model(self):
        """
        Build the sentiment analysis model using scikit-learn
        """
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
        self.model = LogisticRegression(C=1.0, class_weight='balanced', max_iter=1000)
        
        logger.info("Model built")
    
    def train(self, texts, labels, test_size=0.2, random_state=42):
        """
        Train the sentiment analysis model
        
        Args:
            texts (list): List of text samples
            labels (list): List of labels (0: negative, 1: neutral, 2: positive)
            test_size (float): Fraction of data to use for testing
            random_state (int): Random seed for reproducibility
            
        Returns:
            dict: Training results
        """
        # Preprocess texts
        preprocessed_texts = [self.preprocess_text(text) for text in texts]
        
        # Build model if not already built
        if self.model is None or self.vectorizer is None:
            self.build_model()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            preprocessed_texts, labels, test_size=test_size, random_state=random_state, stratify=labels
        )
        
        # Fit vectorizer
        X_train_vec = self.vectorizer.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        X_test_vec = self.vectorizer.transform(X_test)
        accuracy = self.model.score(X_test_vec, y_test)
        
        logger.info(f"Model trained with accuracy: {accuracy:.4f}")
        
        return {
            "accuracy": accuracy,
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        }
    
    def save_model(self, model_path, vectorizer_path):
        """
        Save the model and vectorizer
        
        Args:
            model_path (str): Path to save model
            vectorizer_path (str): Path to save vectorizer
        """
        if self.model is not None:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            logger.info(f"Model saved to {model_path}")
        
        if self.vectorizer is not None:
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            logger.info(f"Vectorizer saved to {vectorizer_path}")
    
    def predict_sentiment(self, text):
        """
        Predict sentiment of input text
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Sentiment prediction with class and confidence
        """
        if self.model is None or self.vectorizer is None:
            logger.error("Model or vectorizer not initialized")
            return {"error": "Model not initialized"}
        
        # Preprocess text
        preprocessed_text = self.preprocess_text(text)
        
        # Vectorize
        text_vec = self.vectorizer.transform([preprocessed_text])
        
        # Predict
        prediction = self.model.predict_proba(text_vec)[0]
        sentiment_class = self.model.predict(text_vec)[0]
        confidence = float(prediction[sentiment_class])
        
        # Map class to sentiment
        sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
        sentiment = sentiment_map[sentiment_class]
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "probabilities": {
                "negative": float(prediction[0]),
                "neutral": float(prediction[1]),
                "positive": float(prediction[2])
            }
        }
    
    def analyze_market_text(self, text):
        """
        Analyze market-related text and provide sentiment analysis
        
        Args:
            text (str): Market-related text
            
        Returns:
            dict: Analysis results
        """
        sentiment = self.predict_sentiment(text)
        
        # If model is not trained yet, provide a rule-based fallback
        if "error" in sentiment:
            # Simple rule-based sentiment analysis as fallback
            positive_words = ['up', 'gain', 'rise', 'bull', 'growth', 'profit', 'positive', 'increase']
            negative_words = ['down', 'loss', 'fall', 'bear', 'decline', 'negative', 'decrease', 'drop']
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                sentiment = {"sentiment": "positive", "confidence": 0.6, "rule_based": True}
            elif negative_count > positive_count:
                sentiment = {"sentiment": "negative", "confidence": 0.6, "rule_based": True}
            else:
                sentiment = {"sentiment": "neutral", "confidence": 0.6, "rule_based": True}
        
        return {
            "text": text,
            "sentiment": sentiment,
            "market_impact": self._assess_market_impact(sentiment)
        }
    
    def _assess_market_impact(self, sentiment):
        """
        Assess potential market impact based on sentiment
        
        Args:
            sentiment (dict): Sentiment prediction
            
        Returns:
            str: Market impact assessment
        """
        if "error" in sentiment:
            return "Unable to assess market impact"
        
        sentiment_value = sentiment["sentiment"]
        confidence = sentiment.get("confidence", 0.5)
        
        if sentiment_value == "positive":
            if confidence > 0.8:
                return "Strongly bullish signal"
            elif confidence > 0.6:
                return "Moderately bullish signal"
            else:
                return "Slightly bullish signal"
        elif sentiment_value == "negative":
            if confidence > 0.8:
                return "Strongly bearish signal"
            elif confidence > 0.6:
                return "Moderately bearish signal"
            else:
                return "Slightly bearish signal"
        else:
            return "Neutral market signal"


# Example usage
if __name__ == "__main__":
    # Create analyzer
    analyzer = MarketSentimentAnalyzer()
    
    # Example texts
    texts = [
        "The market is showing strong growth with increasing volume",
        "Stocks plummeted today as investors reacted to disappointing earnings",
        "Trading remained flat with mixed signals from economic indicators"
    ]
    
    # Analyze each text
    for text in texts:
        result = analyzer.analyze_market_text(text)
        print(f"Text: {result['text']}")
        print(f"Sentiment: {result['sentiment']['sentiment']}")
        print(f"Market Impact: {result['market_impact']}")
        print("-" * 50) 