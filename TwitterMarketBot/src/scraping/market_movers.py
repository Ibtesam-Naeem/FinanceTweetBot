import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging
from scraping.stocks_list import sp500_tickers
import random

logging = setup_logging("MarketMoversLogger")

def convert_market_cap_to_number(market_cap_str):
    """
    Converts a market cap string with suffix (M, B, T, K) to
    a float value in dollars.
    """
    if not market_cap_str:
        return 0

    market_cap_str = market_cap_str.replace(",", "").upper().strip()

    try:
        if market_cap_str in ["-", "N/A", ""]:
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
    
def premarket_data_scraper(driver):
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

    rows = driver.find_elements(By.XPATH, "//div[contains(@class, 'tv-category-content')]//table/tbody/tr")

    for row in rows:
        try:
            ticker_element = row.find_element(By.XPATH, "./td[1]//span")
            ticker_full = ticker_element.text.strip()
            ticker = ticker_full.split("\n")[0]

            if len(ticker) > 1:
                percent_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(2) span")
                percent_change = percent_element.text.strip()
                
                market_cap_element = row.find_element(By.XPATH, "./td[6]")
                market_cap = market_cap_element.text.strip("USD").strip()

                market_cap_value = convert_market_cap_to_number(market_cap)

                if market_cap_value > 5_000_000_000:
                    logging.info(f"Ticker: {ticker}, Market Cap: {market_cap_value}")
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

    final_selection = sp500_stocks + random_non_sp500
    logging.info(f"Total stocks scraped: {len(pre_market_data)}")
    logging.info(f"Total S&P 500 stocks: {len(sp500_stocks)}")
    logging.info(f"Total Non-S&P 500 stocks: {len(non_sp500_stocks)}")
    logging.info(f"Final selection (S&P 500 + 5 random): {len(final_selection)}")

    logging.info("Stocks at 52-week lows (S&P 500 and 5 random others):")
    for stock in final_selection:
        logging.info(f"{stock['Ticker']}: Change: {stock['Pre-Market Change']}: Market Cap: {stock['Market Cap']}")

    return final_selection
