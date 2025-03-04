import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging
from config.db_manager import get_sp500_tickers
import random

logging = setup_logging("MarketMoversLogger")

sp500_tickers = get_sp500_tickers() 

def convert_market_cap_to_number(market_cap_str):
    """
    Converts a market cap string with suffix (M, B, T, K) to
    a float value in dollars.
    """
    if not market_cap_str:
        return 0

    market_cap_str = market_cap_str.replace(",", "").upper().strip()

    try:
        if market_cap_str in ["-", "N/A", "", "—"]:
            return 0
        
        if market_cap_str.endswith("T"):
            return float(market_cap_str[:-1]) * 1_000_000_000_000
        elif market_cap_str.endswith("B"):
            return float(market_cap_str[:-1]) * 1_000_000_000
        elif market_cap_str.endswith("M"):
            return float(market_cap_str[:-1]) * 1_000_000
        elif market_cap_str.endswith("K"):
            return float(market_cap_str[:-1]) * 1_000
        else:
            return float(market_cap_str)
        
    except ValueError as e:
        logging.error(f"Error converting market cap '{market_cap_str}' to number: {e}")
        return 0

def open_premarket_page(url):
    """
    Navigates to the specified pre-market
    page (gainers or losers).
    """
    try:
        driver = chrome_options()
        logging.info(f"Initializing WebDriver and opening page: {url}")

        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-category-content"))
        )

        logging.info(f"Page loaded successfully: {url}")
        return driver

    except Exception as e:
        logging.error(f"Failed to open page {url}: {e}")
        return None
    
def premarket_data_scraper(driver, market_cap_column=6, min_market_cap=5_000_000_000):
    """
    Extracts Pre-Market gainers or losers data from TradingView,
    returns all S&P 500 stocks and 5 random non-S&P 500 stocks.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-category-content"))
    )

    pre_market_data = []
    
    while True:
        try:
            load_more_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "content-D4RPB3ZC"))
            )
            load_more_button.click()
            logging.info("Clicked 'Load More' button. Loading more data.")
            time.sleep(2)
        except:
            logging.info("No more 'Load More' button found. All data loaded.")
            break

    rows = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'tv-category-content')]//table/tbody/tr"
    )

    for row in rows:
        try:
            ticker_element = row.find_element(By.XPATH, "./td[1]//span")
            ticker_full = ticker_element.text.strip()
            ticker = ticker_full.split("\n")[0]

            if len(ticker) > 1:
                percent_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) span")
                percent_change = percent_element.text.strip()
                
                market_cap_element = row.find_element(By.XPATH, f"./td[{market_cap_column}]")
                market_cap = market_cap_element.text.strip("USD").strip()

                market_cap_value = convert_market_cap_to_number(market_cap)

                if market_cap_value > min_market_cap:
                    pre_market_data.append({
                        "Ticker": ticker,
                        "Pre-Market Change": percent_change,
                        "Market Cap": market_cap_value
                    })

        except Exception as e:
            logging.error(f"Error processing row: {e}")

    sp500_stocks = [stock for stock in pre_market_data if stock['Ticker'] in sp500_tickers]
    non_sp500_stocks = [stock for stock in pre_market_data if stock['Ticker'] not in sp500_tickers]
    random_non_sp500 = random.sample(non_sp500_stocks, min(len(non_sp500_stocks), 5))

    return sp500_stocks + random_non_sp500