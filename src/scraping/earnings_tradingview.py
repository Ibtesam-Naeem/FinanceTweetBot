import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging
import time
from config.db_manager import store_earnings_data 
logging = setup_logging("EarningsScraper")

def earnings_to_be_tracked():
    """
    Returns a dictionary mapping days
    of the week to the stocks being tracked.
    """
    return {
        "Monday": {
            "Before Open": ["NOVA", "HUT", "PLUG", "TGTX", "SPHR", "AVDL", "BLFS", "BUR", "RC", "SGRY"],
            "After Close": ["NUSCALE", "OKTRA", "ASTS", "GTLB", "ADMA", "GCT", "SENS", "MRC", "TDUP", "QSI"]
        },
        "Tuesday": {
            "Before Open": ["TGT", "BBY", "SE", "AZO", "PSFE", "EVGO", "ESPR", "GENI", "ONON", "NYAX"],
            "After Close": ["CRWD", "CRDO", "STEM", "JWN", "ORN", "BOX", "ROST", "KIDS", "CHPT", "NPCE"]
        },
        "Wednesday": {
            "Before Open": ["ANG", "FL", "OPFI", "THO", "SSYS", "RSKD", "EDIT", "REVG"],
            "After Close": ["MRVL", "RGTI", "ZS", "MDB", "VEEVA", "VSCO", "TREE", "KGS", "LB", "FSM"]
        },
        "Thursday": {
            "Before Open": ["JD", "CRBL", "KR", "BJ", "DCTH", "BTSH", "NINE", "BKSY", "HIPO", "M"],
            "After Close": ["ACVO", "BBAI", "COST", "GAP", "HPE", "SERV", "IOT", "COO", "CTSO", "VEL"]
        },
        "Friday": {
            "Before Open": ["GCO", "AQN", "WHF", "YPF", "INTT", "ADV", "ONCY"],
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

                    revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
                    revenue_forecast = revenue_forecast_element.text.strip("USD") if revenue_forecast_element else "N/A"

                    try:
                        time_reporting_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_release_next_time']")
                        time_reporting = time_reporting_element.get_attribute("title").strip() if time_reporting_element else "N/A"
                    except:
                        time_reporting = "N/A"

                    earnings_data.append({
                        "Ticker": ticker,
                        "report_date": datetime.datetime.now().date(),
                        "EPS Estimate": eps_estimate,
                        "Revenue Forecast": revenue_forecast,
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
    Scrapes today's earnings from TradingView
    and stores them in the database.
    """
    driver = open_earnings_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return []

    try:
        earnings_data = scrape_earnings_data(driver)

        if earnings_data:
            store_earnings_data(earnings_data)
            logging.info(f"Successfully stored {len(earnings_data)} earnings records in the database.")
        
        return earnings_data

    except Exception as e:
        logging.error(f"Error scraping earnings: {e}.")
        return []
    
    finally:
        driver.quit()