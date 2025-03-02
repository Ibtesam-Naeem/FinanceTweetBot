import os
import requests
from dotenv import load_dotenv
from config.logger import setup_logging

logging = setup_logging("FinnhubScraping")

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

BASE_URL = "https://finnhub.io/api/v1/quote"

INDEX_TICKERS = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI"
}

def get_market_data():
    """
    Fetches the opening and closing price for
    S&P 500 and Dow Jones.
    """
    
    if not FINNHUB_API_KEY:
        logging.error("Finnhub API key is missing.")
        return {}

    data = {}
    
    for index, symbol in INDEX_TICKERS.items():
        try:
            url = f"{BASE_URL}?symbol={symbol}&token={FINNHUB_API_KEY}"
            response = requests.get(url)
            
            if response.status_code != 200:
                logging.warning(f"Failed to fetch data for {index}. HTTP Status: {response.status_code}")
                continue
            
            json_data = response.json()
            
            if "o" not in json_data or "c" not in json_data:
                logging.warning(f"Incomplete data received for {index}.")
                continue
            
            open_price = json_data.get("o", 0)
            close_price = json_data.get("c", 0)
            
            percent_change = ((close_price - open_price) / open_price) * 100 if open_price != 0 else 0
            change_direction = "up" if close_price > open_price else "down"

            data[index] = {
                "Open": open_price,
                "Close": close_price,
                "Change": close_price - open_price,
                "Percent Change": percent_change,
                "Direction": change_direction
            }
            
            logging.info(f"{index} - Open: {open_price}, Close: {close_price}, Change: {data[index]['Change']}, Direction: {change_direction}")
        
        except Exception as e:
            logging.error(f"Error fetching market data for {index}: {e}")

    return data

def get_weekly_data():
    """
    Fetches weekly open (Monday)
    and close (Friday) prices.
    """
    
    if not FINNHUB_API_KEY:
        logging.error("Finnhub API key is missing.")
        return {}

    data = {}
    
    for index, symbol in INDEX_TICKERS.items():
        try:
            url = f"{BASE_URL}?symbol={symbol}&token={FINNHUB_API_KEY}"
            response = requests.get(url)
            
            if response.status_code != 200:
                logging.warning(f"Failed to fetch weekly data for {index}. HTTP Status: {response.status_code}")
                continue
            
            json_data = response.json()
            
            if "o" not in json_data or "c" not in json_data:
                logging.warning(f"Incomplete weekly data received for {index}.")
                continue
            
            monday_open = json_data.get("o", 0)
            friday_close = json_data.get("c", 0)
            
            week_change = friday_close - monday_open
            week_percent_change = (week_change / monday_open) * 100 if monday_open != 0 else 0
            week_direction = "up" if friday_close > monday_open else "down"

            data[index] = {
                "Monday Open": monday_open,
                "Friday Close": friday_close,
                "Weekly Change": week_change,
                "Weekly Percent Change": week_percent_change,
                "Weekly Direction": week_direction
            }
            
            logging.info(f"{index} - Monday Open: {monday_open}, Friday Close: {friday_close}, Weekly Change: {week_change}, Direction: {week_direction}")
        
        except Exception as e:
            logging.error(f"Error fetching weekly market data for {index}: {e}")

    return data