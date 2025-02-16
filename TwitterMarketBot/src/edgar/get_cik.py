import requests
import json
from scraping.earnings_tradingview import get_todays_stocks
from config.logger import setup_logging

logging = setup_logging("CIKlogger")


def fetch_cik_for_tickers(tickers):
    """
    Fetches CIK numbers for a list of stock tickers
    from the SEC API.
    """
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {'User-Agent': "ibtesamnaeemdev@gmail.com"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
    except Exception as e:
        logging.error("Error fetching CIKs.")
        return {}
    
    cik_mapping = {}
    
    for key, value in data.items(): 
        if "cik_str" in value and "ticker" in value:
            formatted_cik = str(value["cik_str"]).zfill(10)  
            cik_mapping[value["ticker"].upper()] = formatted_cik
        
    tickers = list(tickers) 
    results = {}
    
    for ticker in tickers:
        if ticker.upper() in cik_mapping:
            results[ticker.upper()] = cik_mapping[ticker.upper()]
            logging.info(f"Found CIK for {ticker}: {cik_mapping[ticker.upper()]}")
        else:
            logging.error(f"No CIK found for {ticker}")
        
    return results

tickers_to_lookup = get_todays_stocks()
cik_results = fetch_cik_for_tickers(tickers_to_lookup)