"""
FinancialSuite Twitter Bot - Main Entry Point

This script serves as the central entry point for the FinancialSuite Twitter Bot.
It provides functionality to:
1. Set up the environment (download NLTK data, create directories)
2. Train the sentiment analysis model
3. Test the ML functionality
4. Run the Twitter bot with scheduled tweets

Usage:
    python -m src.main --mode [setup|train|test|run|all]
"""

import os
import sys
import argparse
import time
import nltk
from datetime import datetime

# Set up logging
from config.logger import setup_logging
logger = setup_logging("FinancialSuite")

def setup_environment():
    """
    Set up the environment by creating necessary directories and downloading NLTK data
    """
    logger.info("Setting up environment...")
    
    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Download NLTK data
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Fix for punkt_tab resource
        try:
            nltk.data.find('tokenizers/punkt_tab/english/')
        except LookupError:
            # Create a simple workaround for punkt_tab
            punkt_dir = os.path.join(nltk.data.find('tokenizers/punkt'), 'english')
            punkt_tab_dir = os.path.join(nltk.data.path[0], 'tokenizers', 'punkt_tab', 'english')
            os.makedirs(os.path.dirname(punkt_tab_dir), exist_ok=True)
            
            # Create an empty file to satisfy the lookup
            if not os.path.exists(punkt_tab_dir):
                os.makedirs(punkt_tab_dir, exist_ok=True)
                with open(os.path.join(punkt_tab_dir, 'punkt.data'), 'w') as f:
                    f.write('')
            
            logger.info("Created punkt_tab workaround")
        
        logger.info("NLTK data downloaded successfully")
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {e}")
        return False
    
    logger.info("Environment setup completed successfully")
    return True

def train_model():
    """
    Train the sentiment analysis model with market-related text data
    """
    logger.info("Starting model training...")
    
    try:
        from ml.train_model import train_sentiment_model
        analyzer = train_sentiment_model()
        logger.info("Model training completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return False

def test_ml():
    """
    Test the ML functionality by analyzing sample texts and generating a sample tweet
    """
    logger.info("Testing ML functionality...")
    
    try:
        # Import the test module and run tests
        from test_ml import test_sentiment_analyzer, test_market_sentiment_tweet
        
        # Test sentiment analyzer
        test_sentiment_analyzer()
        
        # Test tweet generation
        test_market_sentiment_tweet()
        
        logger.info("ML testing completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error testing ML functionality: {e}")
        return False

def run_bot():
    """
    Run the Twitter bot with scheduled tweets
    """
    logger.info("Starting Twitter bot...")
    
    try:
        # Import the Twitter bot module
        from twitter.bot import run_twitter_bot
        
        # Run the Twitter bot
        run_twitter_bot()
        
        return True
    except Exception as e:
        logger.error(f"Error running Twitter bot: {e}")
        return False

def main():
    """
    Main function to parse command line arguments and run the appropriate function
    """
    parser = argparse.ArgumentParser(description='FinancialSuite Twitter Bot')
    parser.add_argument('--mode', type=str, default='all',
                        choices=['setup', 'train', 'test', 'run', 'all'],
                        help='Operation mode: setup, train, test, run, or all')
    
    args = parser.parse_args()
    
    # Run the appropriate function based on the mode
    if args.mode == 'setup' or args.mode == 'all':
        if not setup_environment():
            logger.error("Environment setup failed")
            if args.mode == 'setup':
                return
    
    if args.mode == 'train' or args.mode == 'all':
        if not train_model():
            logger.error("Model training failed")
            if args.mode == 'train':
                return
    
    if args.mode == 'test' or args.mode == 'all':
        if not test_ml():
            logger.error("ML testing failed")
            if args.mode == 'test':
                return
    
    if args.mode == 'run' or args.mode == 'all':
        if not run_bot():
            logger.error("Twitter bot failed to run")
            return

if __name__ == "__main__":
    main()