"""
Twitter bot implementation
"""
import os
import time
import schedule
import tweepy
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Callable, Optional

from src.config.api_client import (
    get_economic_events,
    get_earnings,
    get_fear_greed,
    get_premarket_movers,
    get_all_time_highs
)

from src.twitter.tweet_format import (
    daily_premkt_earnings_tweet,
    daily_afterhrs_earnings_tweet,
    econ_reminder_tomorrow,
    econ_reminder_weekly,
    pre_market_gainer,
    pre_market_losers,
    all_time_high,
    fear_sentiment
)

from src.ml import get_market_sentiment_tweet
from src.config.logger import setup_logging
from src.config.settings import SCHEDULER_SLEEP_INTERVAL, MAX_ITEMS_PER_TWEET
from src.utils.error_handling import retry

logger = setup_logging("TwitterBot")

class TwitterBot:
    """Twitter bot for posting financial market updates"""
    
    def __init__(self):
        """Initialize the Twitter bot"""
        self.client = None
        self.initialize_client()
    
    def initialize_client(self) -> bool:
        """Initialize the Twitter API client"""
        # Load environment variables
        load_dotenv()
        
        # Get Twitter API credentials
        api_key = os.getenv("API_KEY")
        api_secret = os.getenv("API_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        bearer_token = os.getenv("BEARER_TOKEN")
        
        if not all([api_key, api_secret, access_token, access_token_secret, bearer_token]):
            logger.error("Twitter API credentials not found in .env file")
            return False
        
        # Initialize Twitter client
        try:
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )
            logger.info("Twitter client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {e}")
            return False
    
    @retry(max_tries=3, delay_seconds=5)
    def send_tweet(self, tweet_text: str) -> bool:
        """
        Send a tweet via the Twitter API
        
        Args:
            tweet_text (str): Tweet content
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not tweet_text:
            logger.info("No tweet content to send")
            return False
        
        if not self.client:
            logger.error("Twitter client not initialized")
            return False
        
        try:
            response = self.client.create_tweet(text=tweet_text)
            logger.info(f"Tweet sent successfully: {tweet_text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Error sending tweet: {e}")
            return False
    
    def schedule_tweets(self):
        """Set up the tweet schedule"""
        logger.info("Setting up tweet schedule...")
        
        # Pre-market tweets
        schedule.every().day.at("08:00").do(self.post_pre_market_earnings_tweet)
        schedule.every().day.at("08:30").do(self.post_pre_market_gainers_tweet)
        schedule.every().day.at("08:35").do(self.post_pre_market_losers_tweet)
        
        # Market open tweets
        schedule.every().day.at("09:30").do(self.post_fear_sentiment_tweet)
        
        # Mid-day tweets
        schedule.every().day.at("11:00").do(self.post_market_sentiment_tweet)
        schedule.every().day.at("12:00").do(self.post_after_hours_earnings_tweet)
        
        # Afternoon tweets
        schedule.every().day.at("15:00").do(self.post_market_sentiment_tweet)
        
        # After market close tweets
        schedule.every().day.at("16:15").do(self.post_all_time_high_tweet)
        
        # Evening tweets
        schedule.every().day.at("18:00").do(self.post_daily_econ_tweet)
        
        # Weekly tweets
        schedule.every().sunday.at("18:00").do(self.post_weekly_econ_tweet)
        
        logger.info("Tweet schedule set up successfully")
    
    def run(self):
        """Run the Twitter bot"""
        if not self.client:
            if not self.initialize_client():
                logger.error("Failed to initialize Twitter client")
                return False
        
        self.schedule_tweets()
        logger.info("Twitter bot started")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(SCHEDULER_SLEEP_INTERVAL)
        except KeyboardInterrupt:
            logger.info("Twitter bot stopped by user")
        except Exception as e:
            logger.error(f"Twitter bot stopped due to error: {e}")
            return False
        
        return True
    
    # Tweet posting methods
    def post_pre_market_earnings_tweet(self):
        """Post pre-market earnings tweet"""
        try:
            earnings_data = get_earnings()
            pre_market_earnings = [e for e in earnings_data if e["Time"] == "Before Open"]
            
            # Process and sort data
            pre_market_earnings = self._process_earnings_data(pre_market_earnings)
            
            if pre_market_earnings:
                tweet = daily_premkt_earnings_tweet(pre_market_earnings[:MAX_ITEMS_PER_TWEET])
                self.send_tweet(tweet)
            else:
                logger.info("No pre-market earnings available")
        except Exception as e:
            logger.error(f"Error posting pre-market earnings tweet: {e}")
    
    def post_after_hours_earnings_tweet(self):
        """Post after-hours earnings tweet"""
        try:
            earnings_data = get_earnings()
            after_hours_earnings = [e for e in earnings_data if e["Time"] == "After Close"]
            
            # Sort by market cap if available
            try:
                for earning in after_hours_earnings:
                    if "Market Cap" in earning:
                        market_cap_str = earning["Market Cap"].replace("$", "").replace(",", "")
                        if "B" in market_cap_str:
                            market_cap_str = market_cap_str.replace("B", "")
                            earning["Market Cap Numeric"] = float(market_cap_str) * 1_000_000_000
                        elif "M" in market_cap_str:
                            market_cap_str = market_cap_str.replace("M", "")
                            earning["Market Cap Numeric"] = float(market_cap_str) * 1_000_000
                        else:
                            earning["Market Cap Numeric"] = float(market_cap_str)
                    else:
                        earning["Market Cap Numeric"] = 0
            
                after_hours_earnings.sort(key=lambda x: x.get("Market Cap Numeric", 0), reverse=True)
            except Exception as e:
                logger.warning(f"Error sorting earnings by market cap: {e}")
            
            # Take only the top 5
            after_hours_earnings = after_hours_earnings[:5]
            
            if after_hours_earnings:
                tweet = daily_afterhrs_earnings_tweet(after_hours_earnings)
                self.send_tweet(tweet)
            else:
                logger.info("No After-Hours earnings available.")
        except Exception as e:
            logger.error(f"Error posting after-hours earnings tweet: {e}")
    
    def post_daily_econ_tweet(self):
        """Post daily economic events tweet"""
        try:
            economic_events = get_economic_events()
            if economic_events:
                tweet = econ_reminder_tomorrow(economic_events)
                self.send_tweet(tweet)
            else:
                logger.info("No economic events available.")
        except Exception as e:
            logger.error(f"Error posting daily economic tweet: {e}")
    
    def post_weekly_econ_tweet(self):
        """Post weekly economic events tweet"""
        try:
            economic_events = get_economic_events(limit=50)
            
            # Filter events for the upcoming week
            today = datetime.now().date()
            one_week_later = today + timedelta(days=7)
            
            try:
                weekly_events = []
                for event in economic_events:
                    if "Date" in event:
                        event_date_str = event["Date"].split("T")[0]
                        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
                        
                        if today < event_date <= one_week_later:
                            weekly_events.append(event)
            
                economic_events = weekly_events
            except Exception as e:
                logger.warning(f"Error filtering weekly economic events: {e}")
            
            if economic_events:
                tweet = econ_reminder_weekly(economic_events)
                self.send_tweet(tweet)
            else:
                logger.info("No economic events available for the week.")
        except Exception as e:
            logger.error(f"Error posting weekly economic tweet: {e}")
    
    def post_pre_market_gainers_tweet(self):
        """Post pre-market gainers tweet"""
        try:
            premarket_data = get_premarket_movers()
            if premarket_data and "gainers" in premarket_data:
                tweet = pre_market_gainer(premarket_data["gainers"])
                self.send_tweet(tweet)
            else:
                logger.info("No pre-market gainers available.")
        except Exception as e:
            logger.error(f"Error posting pre-market gainers tweet: {e}")
    
    def post_pre_market_losers_tweet(self):
        """Post pre-market losers tweet"""
        try:
            premarket_data = get_premarket_movers()
            if premarket_data and "losers" in premarket_data:
                tweet = pre_market_losers(premarket_data["losers"])
                self.send_tweet(tweet)
            else:
                logger.info("No pre-market losers available.")
        except Exception as e:
            logger.error(f"Error posting pre-market losers tweet: {e}")
    
    def post_fear_sentiment_tweet(self):
        """Post fear & greed sentiment tweet"""
        try:
            fear_data = get_fear_greed()
            if fear_data:
                tweet = fear_sentiment(fear_data)
                self.send_tweet(tweet)
            else:
                logger.info("No fear & greed data available.")
        except Exception as e:
            logger.error(f"Error posting fear sentiment tweet: {e}")
    
    def post_all_time_high_tweet(self):
        """Post all-time high stocks tweet"""
        try:
            ath_data = get_all_time_highs()
            if ath_data:
                tweet = all_time_high(ath_data)
                self.send_tweet(tweet)
            else:
                logger.info("No all-time high data available.")
        except Exception as e:
            logger.error(f"Error posting all-time high tweet: {e}")
    
    def post_market_sentiment_tweet(self):
        """Post AI-powered market sentiment tweet"""
        try:
            tweet_text = get_market_sentiment_tweet()
            if tweet_text:
                self.send_tweet(tweet_text)
                logger.info("Posted market sentiment tweet successfully")
            else:
                logger.warning("No market sentiment tweet generated")
        except Exception as e:
            logger.error(f"Error posting market sentiment tweet: {e}")
    
    def _process_earnings_data(self, earnings_data):
        """Process and sort earnings data by market cap"""
        try:
            for earning in earnings_data:
                if "Market Cap" in earning:
                    market_cap_str = earning["Market Cap"].replace("$", "").replace(",", "")
                    if "B" in market_cap_str:
                        market_cap_str = market_cap_str.replace("B", "")
                        earning["Market Cap Numeric"] = float(market_cap_str) * 1_000_000_000
                    elif "M" in market_cap_str:
                        market_cap_str = market_cap_str.replace("M", "")
                        earning["Market Cap Numeric"] = float(market_cap_str) * 1_000_000
                    else:
                        earning["Market Cap Numeric"] = float(market_cap_str)
                else:
                    earning["Market Cap Numeric"] = 0
            
            # Sort by market cap (descending)
            earnings_data.sort(key=lambda x: x.get("Market Cap Numeric", 0), reverse=True)
            return earnings_data
        except Exception as e:
            logger.warning(f"Error processing earnings data: {e}")
            return earnings_data

# Function to run the Twitter bot
def run_twitter_bot():
    """Run the Twitter bot"""
    bot = TwitterBot()
    return bot.run() 