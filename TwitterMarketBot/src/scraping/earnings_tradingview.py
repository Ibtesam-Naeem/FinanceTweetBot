import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging
import time
logging = setup_logging("EarningsScraper")

def earnings_to_be_tracked():
    """
    Returns a dictionary mapping days
    of the week to the stocks being tracked.
    First line: Before Open
    Second line: After Close
    """
    return {
        "Monday": {
            "Before Open": ["DPZ", "BRK.B", "AZUL", "BCRX", "KSPI", "LINC", "SMMT", "WLK", "SSL", "CCO"],
            "After Close": ["HIMS", "RIOT", "TEMP", "CLF", "ZM", "FANG", "CTRA", "O", "CHGG", "TCOM"]
        },
        "Tuesday": {
            "Before Open": ["HD", "PLNT", "KDP", "DOCN", "ALLT", "CIFR", "BNS", "DNUT", "ITRI", "AMT"],
            "After Close": ["CAVA", "AMC", "AXON", "FSLR", "LCID", "CART", "LMND", "WDAY", "ZETA", "INTU"]
        },
        "Wednesday": {
            "Before Open": ["LOW", "NRG", "AAP", "YOU", "BYD", "STLA", "IEP", "INVZ", "VLN", "UWMC"],
            "After Close": ["NVDA", "SNOW", "AI", "CRM", "MARA", "JOBY", "IONQ", "ROOT", "KTOS", "NTNX"]
        },
        "Thursday": {
            "Before Open": ["VST", "NCLH", "GEO", "GTN", "VTRS", "VRNA", "TD", "MPW", "OPRA", "DQ"],
            "After Close": ["SOUN", "DELL", "RKLB", "ACHR", "CLOV", "SMR", "TMDX", "DUOL", "TLN", "OPEN"]
        },
        "Friday": {
            "Before Open": ["FUBO", "WULF", "GTLS", "FLGT", "AES", "FRO", "BFLY", "AMR", "DIBS", "APLS"],
            "After Close": []
        }
    }

def get_todays_stocks():
    """
    Returns two sets of stocks:
    - before_open_stocks: Stocks reporting before the open
    - after_close_stocks: Stocks reporting after the close
    """
    today = datetime.datetime.now().strftime("%A")
    tracked_stocks = earnings_to_be_tracked().get(today, {})

    before_open_stocks = set(tracked_stocks.get("Before Open", []))
    after_close_stocks = set(tracked_stocks.get("After Close", []))

    return before_open_stocks, after_close_stocks

def open_earnings_calendar():
    """
    Navigates to the Trading View
    Earnings calendar page.
    """
    try:
        driver = chrome_options()
        logging.info("Initializing WebDriver and opening earnings calendar page.")

        driver.get("https://www.tradingview.com/markets/stocks-usa/earnings/")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
        )

        logging.info("Earnings calendar page loaded successfully.")
        return driver

    except Exception as e:
        logging.error(f"Failed to open earnings calendar: {e}")
        return None

def scrape_earnings_data(driver):
    """
    Extracts earnings data from TradingView and filters
    for today's tracked stocks.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
    )

    while True:
        try:
            load_more_button = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tv-load-more__btn"))
            )
            load_more_button.click()
            logging.info("Clicked 'Load More' button. Loading more data.")
            time.sleep(1)

        except Exception as e:
            logging.info("No 'Load More' button found.")
            break
        
    earnings_data = []

    before_open_stocks, after_close_stocks = get_todays_stocks()

    def process_stocks(stock_set):
        index = 0
        while True:
            try:
                rows = driver.find_elements(By.CLASS_NAME, "tv-data-table__row")
                
                if index >= len(rows):
                    break
                
                row = rows[index]

                ticker_element = WebDriverWait(row, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-field-key='name']"))
                )
                ticker_full = ticker_element.text.strip()
                ticker_d = ticker_full.split("\n")[0]
                ticker = "".join(ticker_d[:-1])

                if ticker in stock_set:
                    eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
                    eps_estimate = eps_estimate_element.text.strip("USD") if eps_estimate_element else "N/A"

                    reported_eps_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_fq']")
                    reported_eps = reported_eps_element.text.strip("USD") if reported_eps_element else "N/A"

                    revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
                    revenue_forecast = revenue_forecast_element.text.strip("USD") if revenue_forecast_element else "N/A"

                    reported_revenue_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_fq']")
                    reported_revenue = reported_revenue_element.text.strip("USD") if reported_revenue_element else "N/A"
                    try:
                        time_reporting_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_release_next_time']")
                        time_reporting = time_reporting_element.get_attribute("title").strip() if time_reporting_element else "N/A"
                    except:
                        time_reporting = "N/A"

                    earnings_data.append({
                        "Ticker": ticker,
                        "EPS Estimate": eps_estimate,
                        "Reported EPS": reported_eps,
                        "Revenue Forecast": revenue_forecast,
                        "Reported Revenue": reported_revenue,
                        "Time": time_reporting
                    })

                index += 1

            except Exception as e:
                logging.error(f"Error processing row: {e}")
                index += 1

    logging.info("Checking earnings for Before Open stocks first.")
    process_stocks(before_open_stocks)

    logging.info("Checking earnings for After Close stocks.")
    process_stocks(after_close_stocks)

    return earnings_data

def scrape_todays_earnings():
    """
    Scrapes today's earnings
    from TradingView.
    """
    driver = open_earnings_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return []

    try:
        return scrape_earnings_data(driver)

    except Exception as e:
        logging.error(f"Error scraping earnings: {e}.")
        return []
    
    finally:
        driver.quit()
