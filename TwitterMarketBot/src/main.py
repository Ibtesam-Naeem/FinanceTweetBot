import os
import time
import schedule
import tweepy
from dotenv import load_dotenv

from scraping.earnings_tradingview import scrape_todays_earnings
from scraping.econ_scraper import (
    open_earnings_calendar,
    click_importance,
    day,
    scrape_economics_data,
)
from scraping.market_movers import open_premarket_page, premarket_data_scraper
from scraping.sentiment import fear_index
from scraping.closing_prices import get_market_data, get_weekly_data
from scraping.general_info import trading_holidays
from twitter.tweet_format import (
    daily_premkt_earnings_tweet,
    daily_afterhrs_earnings_tweet,
    econ_reminder_tomorrow,
    econ_reminder_weekly,
    pre_market_gainer,
    pre_market_losers,
    week_high_52,
    week_low_52,
    all_time_high,
    all_time_low,
    pre_market_gap,
    fear_sentiment,
    daily_market_summary,
    weekly_market_summary,
    closures,
)

from config.logger import setup_logging

logging = setup_logging("TwitterBot")
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

def send_tweet(tweet_text):
    """
    Helper function to send a tweet via the Twitter API.
    """
    if tweet_text:
        try:
            response = client.create_tweet(text=tweet_text)
            logging.info(f"Tweet sent successfully: {tweet_text[:50]}...")
        except Exception as e:
            logging.error(f"Error sending tweet: {e}")
    else:
        logging.info("No tweet content to send.")

def post_pre_market_earnings_tweet():
    """
    Fetches earnings data, formats the Pre-Market tweet,
    and sends it.
    Scheduled for 4:00 AM.
    """
    earnings_data = scrape_todays_earnings()
    pre_market_earnings = [e for e in earnings_data if e["Time"] == "Before Open"]

    if pre_market_earnings:
        tweet = daily_premkt_earnings_tweet(pre_market_earnings)
        send_tweet(tweet)
    else:
        logging.info("No Pre-Market earnings available.")

def post_after_hours_earnings_tweet():
    """
    Fetches earnings data, formats the After-Hours tweet,
    and sends it.
    Scheduled for 12:00 PM.
    """
    earnings_data = scrape_todays_earnings()
    after_hours_earnings = [e for e in earnings_data if e["Time"] == "After Close"]

    if after_hours_earnings:
        tweet = daily_afterhrs_earnings_tweet(after_hours_earnings)
        send_tweet(tweet)
    else:
        logging.info("No After-Hours earnings available.")

def post_daily_econ_tweet():
    """
    Fetches economic data for tomorrow, formats the tweet,
    and sends it.
    Scheduled for 8:00 PM.
    """
    driver = open_earnings_calendar()
    if driver:
        click_importance(driver)
        day(driver, "Tomorrow")
        time.sleep(1)
        econ_data_tomorrow = scrape_economics_data(driver)
        tweet = econ_reminder_tomorrow(econ_data_tomorrow)
        send_tweet(tweet)
        driver.quit()

def post_weekly_econ_tweet():
    """
    Fetches economic data for this week, formats the tweet,
    and sends it.
    Scheduled for 10:00 PM.
    """
    driver = open_earnings_calendar()
    if driver:
        click_importance(driver)
        day(driver, "This Week")
        time.sleep(1)
        econ_data_week = scrape_economics_data(driver)
        tweet = econ_reminder_weekly(econ_data_week)
        send_tweet(tweet)
        driver.quit()

def post_pre_market_gainers_tweet():
    """
    Fetches and sends the Pre-Market Gainers tweet.
    Scheduled for 7:00 AM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/"
    )
    if driver:
        gainers_data = premarket_data_scraper(driver)
        tweet = pre_market_gainer(gainers_data)
        send_tweet(tweet)
        driver.quit()

def post_pre_market_losers_tweet():
    """
    Fetches and sends the Pre-Market Losers tweet.
    Scheduled for 7:05 AM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-losers/"
    )
    if driver:
        losers_data = premarket_data_scraper(driver)
        tweet = pre_market_losers(losers_data)
        send_tweet(tweet)
        driver.quit()

def post_week_high_52_tweet():
    """
    Fetches and sends the 52-Week Highs tweet.
    Scheduled for 3:45 PM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-high/"
    )
    if driver:
        high_52_data = premarket_data_scraper(driver)
        tweet = week_high_52(high_52_data)
        send_tweet(tweet)
        driver.quit()

def post_week_low_52_tweet():
    """
    Fetches and sends the 52-Week Lows tweet.
    Scheduled for 3:46 PM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-52wk-low/"
    )
    if driver:
        low_52_data = premarket_data_scraper(driver)
        tweet = week_low_52(low_52_data)
        send_tweet(tweet)
        driver.quit()

def post_all_time_high_tweet():
    """
    Fetches and sends the All-Time Highs tweet.
    Scheduled for 3:50 PM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-ath/"
    )
    if driver:
        all_time_high_data = premarket_data_scraper(driver)
        tweet = all_time_high(all_time_high_data)
        send_tweet(tweet)
        driver.quit()

def post_all_time_low_tweet():
    """
    Fetches and sends the All-Time Lows tweet.
    Scheduled for 3:51 PM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-atl/"
    )
    if driver:
        all_time_low_data = premarket_data_scraper(driver)
        tweet = all_time_low(all_time_low_data)
        send_tweet(tweet)
        driver.quit()

def post_gap_tweet():
    """
    Fetches and sends the Pre-Market Gap tweet.
    Scheduled for 8:00 AM.
    """
    driver = open_premarket_page(
        "https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gappers/"
    )
    if driver:
        gap_data = premarket_data_scraper(driver)
        tweet = pre_market_gap(gap_data)
        send_tweet(tweet)
        driver.quit()

def post_roaring_kitty_tweet():
    """
    Fetches and sends the roaring kitty tweet
    """

def post_fear_sentiment():
    """
    Scrapes the Fear & Greed Index, formats a tweet, and posts it.
    """
    fear_data = fear_index()

    if fear_data and len(fear_data) > 0:
        tweet = fear_sentiment(fear_data)
        send_tweet(tweet)
    else:
        logging.error("Failed to retrieve Fear & Greed Index data.")

def post_daily_market_summary():
    """
    Fetches daily market data, formats the summary tweet,
    and sends it.
    Scheduled for 4:10 PM.
    """
    market_data = get_market_data()
    
    if market_data:
        tweet = daily_market_summary(market_data)
        send_tweet(tweet)
    else:
        logging.error("No market data available for daily summary.")

def post_weekly_market_summary():
    """
    Fetches weekly market data, formats the summary tweet,
    and sends it.
    Scheduled for Friday 4:15 PM.
    """
    weekly_data = get_weekly_data()
    
    if weekly_data:
        tweet = weekly_market_summary(weekly_data)
        send_tweet(tweet)
    else:
        logging.error("No market data available for weekly summary.")

def post_trading_holiday():
    """
    Fetches the trading holiday tweet and sends it
    If holiday, post day prior at 8 PM
    """
    closing_dates = trading_holidays()

    if closing_dates:
        tweet = closures(closing_dates)
        send_tweet()
    else:
        logging.error("No Holiday Tomorrow")
        
if __name__ == "__main__":
    logging.info("Starting Twitter Bot Scheduler...")

    schedule.every().day.at("04:45").do(post_pre_market_earnings_tweet)  # 4:45 AM
    schedule.every().day.at("07:00").do(post_pre_market_gainers_tweet)   # 7:00 AM
    schedule.every().day.at("07:05").do(post_pre_market_losers_tweet)    # 7:05 AM
    schedule.every().day.at("08:00").do(post_gap_tweet)                  # 9:00 AM
    schedule.every().day.at("12:00").do(post_after_hours_earnings_tweet) # 12:00 PM
    schedule.every().day.at("15:45").do(post_week_high_52_tweet)         # 3:45 PM
    schedule.every().day.at("15:46").do(post_week_low_52_tweet)          # 3:46 PM
    schedule.every().day.at("15:50").do(post_all_time_high_tweet)        # 3:50 PM
    schedule.every().day.at("15:51").do(post_all_time_low_tweet)         # 3:51 PM
    schedule.every().day.at("23:00").do(post_daily_econ_tweet)           # 11:00 PM
    schedule.every().day.at("22:00").do(post_weekly_econ_tweet)          # 10:00 PM
    schedule.every().hour.do(post_fear_sentiment)                        # every hour
    schedule.every().day.at("16:05").do(post_daily_market_summary)
    schedule.every().friday.at("16:20").do(post_weekly_market_summary)
    
    while True:
        schedule.run_pending()
        time.sleep(30)

