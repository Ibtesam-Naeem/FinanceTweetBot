import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from src.config.logger import setup_logging
from src.config.settings import TWITTER_API_RETRY_COUNT, TWITTER_API_RETRY_DELAY

load_dotenv()
logger = setup_logging("APIClient")

BACKEND_URL = os.getenv("BACKEND_URL")

class APIError(Exception):
    """Exception raised for API errors"""
    pass

@retry(max_tries=TWITTER_API_RETRY_COUNT, delay_seconds=TWITTER_API_RETRY_DELAY)
def api_request(endpoint: str, method: str = "GET", params: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make an API request to the backend
    
    Args:
        endpoint (str): API endpoint
        method (str): HTTP method (GET, POST, etc.)
        params (dict, optional): Request parameters
        
    Returns:
        dict: API response data
        
    Raises:
        APIError: If the API request fails
    """
    if not BACKEND_URL:
        raise APIError("BACKEND_URL environment variable not set")
    
    url = f"{BACKEND_URL}/{endpoint.lstrip('/')}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, json=params)
        else:
            raise APIError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise APIError(f"API request failed: {e}")

def get_economic_events(limit: int = 10) -> List[Dict[str, Any]]:
    """Get economic events from the backend API"""
    try:
        return api_request("economic-events", params={"limit": limit})
    except APIError as e:
        logger.error(f"Failed to fetch economic events: {e}")
        return []

def get_earnings(limit: int = 10) -> List[Dict[str, Any]]:
    """Get earnings data from the backend API"""
    try:
        return api_request("earnings", params={"limit": limit})
    except APIError as e:
        logger.error(f"Failed to fetch earnings: {e}")
        return []

def get_fear_greed() -> Dict[str, Any]:
    """Get fear & greed index from the backend API"""
    try:
        return api_request("fear-greed")
    except APIError as e:
        logger.error(f"Failed to fetch fear & greed index: {e}")
        raise

def get_premarket_movers() -> Dict[str, Any]:
    """Get pre-market movers from the backend API"""
    try:
        return api_request("premarket")
    except APIError as e:
        logger.error(f"Failed to fetch pre-market movers: {e}")
        raise

def get_52_week_highs() -> List[Dict[str, Any]]:
    """Get stocks at 52-week highs from the backend API"""
    try:
        return api_request("market-data/52-week-highs")
    except APIError as e:
        logger.error(f"Failed to fetch 52-week highs: {e}")
        raise

def get_52_week_lows() -> List[Dict[str, Any]]:
    """Get stocks at 52-week lows from the backend API"""
    try:
        return api_request("market-data/52-week-lows")
    except APIError as e:
        logger.error(f"Failed to fetch 52-week lows: {e}")
        raise

def get_all_time_highs() -> List[Dict[str, Any]]:
    """Get stocks at all-time highs from the backend API"""
    try:
        return api_request("market-data/all-time-highs")
    except APIError as e:
        logger.error(f"Failed to fetch all-time highs: {e}")
        raise

def get_gap_stocks() -> List[Dict[str, Any]]:
    """Get stocks with significant price gaps from the backend API"""
    try:
        return api_request("market-data/gaps")
    except APIError as e:
        logger.error(f"Failed to fetch gap stocks: {e}")
        raise

def get_daily_market_summary() -> Dict[str, Any]:
    """Get daily market summary from the backend API"""
    try:
        return api_request("market-data/daily-summary")
    except APIError as e:
        logger.error(f"Failed to fetch daily market summary: {e}")
        raise

def get_weekly_market_summary() -> Dict[str, Any]:
    """
    Gets the weekly market summary from the backend API
    """
    try:
        return api_request("market-data/weekly-summary")
    except APIError as e:
        logger.error(f"Failed to fetch weekly market summary: {e}")
        raise

def get_trading_holidays() -> List[Dict[str, Any]]:
    """
    Gets the trading holidays from the backend API
    """
    try:
        return api_request("market-data/trading-holidays")
    except APIError as e:
        logger.error(f"Failed to fetch trading holidays: {e}")
        raise 