import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging
import time
from config.db_manager import store_earnings_data 

logging = setup_logging("EarningsScraper")

ALL_STOCKS = [
    "NOVA", "HUT", "PLUG", "TGTX", "SPHR", "AVDL", "BLFS", "BUR", "RC", "SGRY",
    "NUSCALE", "OKTRA", "ASTS", "GTLB", "ADMA", "GCT", "SENS", "MRC", "TDUP", "QSI",
    "TGT", "BBY", "SE", "AZO", "PSFE", "EVGO", "ESPR", "GENI", "ONON", "NYAX",
    "CRWD", "CRDO", "STEM", "JWN", "ORN", "BOX", "ROST", "KIDS", "CHPT", "NPCE",
    "ANG", "FL", "OPFI", "THO", "SSYS", "RSKD", "EDIT", "REVG",
    "MRVL", "RGTI", "ZS", "MDB", "VEEVA", "VSCO", "TREE", "KGS", "LB", "FSM",
    "JD", "CRBL", "KR", "BJ", "DCTH", "BTSH", "NINE", "BKSY", "HIPO", "M",
    "ACVO", "BBAI", "COST", "GAP", "HPE", "SERV", "IOT", "COO", "CTSO", "VEL",
    "GCO", "AQN", "WHF", "YPF", "INTT", "ADV", "ONCY"
]

def open_earnings_calendar():
    """
    Navigates to the Trading View Earnings calendar page.
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
    Extracts earnings data from TradingView
    for all tracked stocks.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'itemContent-LeZwGiB6') and contains(text(), 'This Week')]"))
        )
        this_week_button = driver.find_element(By.XPATH, "//div[contains(@class, 'itemContent-LeZwGiB6') and contains(text(), 'This Week')]")
        this_week_button.click()
        logging.info("Clicked on 'This Week' button.")
    
    except Exception as e:
        logging.error(f"Failed to click on 'This Week' button: {e}")

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

        except Exception:
            logging.info("No 'Load More' button found.")
            break
        
    earnings_data = []
    tracked_stocks = set(ALL_STOCKS)
    logging.info(f"Scraping earnings for {len(tracked_stocks)} tracked stocks.")

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

            if ticker in tracked_stocks:
                eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
                eps_estimate = eps_estimate_element.text.strip("USD") if eps_estimate_element else "N/A"

                revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
                revenue_forecast = revenue_forecast_element.text.strip("USD") if revenue_forecast_element else "N/A"

                try:
                    time_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_release_next_time']")
                    time_reporting = time_element.get_attribute("title").strip()
                    
                    if not time_reporting:
                        time_reporting = "Unknown"
                        logging.warning(f"Time missing for {ticker}, setting as 'Unknown'.")
                
                except Exception as e:
                    logging.error(f"Error extracting time for {ticker}: {e}")
                    time_reporting = "Unknown"

                date_reporting_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_release_next_date']")
                date_reporting = date_reporting_element.text.strip() if date_reporting_element else "N/A"

                earnings_data.append({
                    "Ticker": ticker,
                    "report_date": date_reporting,
                    "EPS Estimate": eps_estimate,
                    "Revenue Forecast": revenue_forecast,
                    "Time": time_reporting
                })
                logging.info(f"Found earnings data for {ticker} on {date_reporting} at {time_reporting}")

            index += 1

        except Exception as e:
            logging.error(f"Error processing row {index}: {e}")
            index += 1

    return earnings_data

def scrape_all_earnings():
    """
    Scrapes all earnings from TradingView
    and stores them in the database.
    """
    driver = open_earnings_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return []

    earnings_data = [] 

    try:
        earnings_data = scrape_earnings_data(driver)

        if earnings_data:
            try:
                store_earnings_data(earnings_data)
                logging.info(f"Successfully stored {len(earnings_data)} earnings records in the database.")
            except Exception as db_error:
                logging.error(f"Failed to store earnings in database: {db_error}")

        return earnings_data

    except Exception as e:
        logging.error(f"Error scraping earnings: {e}")
        return earnings_data 
    
    finally:
        driver.quit()