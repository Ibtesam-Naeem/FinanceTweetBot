import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging
import time
import heapq

logging = setup_logging("EarningsScraper")

def earnings_to_be_tracked():
    """
    Returns a dictionary mapping days
    of the week to the stocks being tracked.
    """
    return {
        "Monday": ["RIG", "NE", "UFPI", "JELD", "JW", "HUN", "OTTR", "TNC"],
        "Tuesday": ["BIDU", "GENE", "AXSM", "MDT", "ETR", "FLR", "WSO", "EXPD", "SPNS", "CAG", 
                    "ARISTA", "OXY", "DVN", "TOL", "HALO", "MTDR", "UIS", "CE", "SBLK", "CNS", "CDNS"],
        "Wednesday": ["ETSY", "SEDG", "GRMN", "WIX", "FVRR", "GLBE", "TECK", "ADI", "KRYS", "WING",
                      "CVNA", "TOST", "ENVX", "CAKE", "BMRN", "EXAS", "BHC", "VALE", "NYMT", "CDE"],
        "Thursday": ["BABA", "WMT", "U", "W", "CCJ", "BAX", "NICE", "JUMIA", "SHAK", "LNG", 
                     "RIVN", "SQ", "NEM", "INOD", "BKNG", "TXRH", "GNT", "FIVN", "DBX"],
        "Friday": ["ABR", "ATMU", "ASIX", "SHO", "UNIT", "TXNM", "VIPS", "USM", "BRC", "OIS"]
    }

def get_todays_stocks():
    """
    Returns the stock list for today's earnings
    """
    today = datetime.datetime.now().strftime("%A")
    tracked_stocks = earnings_to_be_tracked().get(today, [])
    return set(tracked_stocks)

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
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
    )

    earnings_data = []
    tracked_stocks = get_todays_stocks()

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

    return earnings_data

def get_top_5_after_close(earnings_data):
    """
    Get top 5 stocks by Market Cap reporting After Close
    using a Min-Heap for efficient selection.
    """
    min_heap = []

    for stock in earnings_data:
        if stock["Time"] == "After Close" and stock["Market Cap"]:
            heapq.heappush(min_heap, (stock["Market Cap"], stock))
            if len(min_heap) > 5:
                heapq.heappop(min_heap)
    
    top_5 = [stock for _, stock in sorted(min_heap, reverse=True)]
    return top_5

def scrape_todays_earnings():
    """
    Scrapes today's earnings from TradingView
    and selects the top 3 by Market Cap.
    """
    driver = open_earnings_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return []

    try:
        earnings_data = scrape_earnings_data(driver)
        top_5_stocks = get_top_5_after_close(earnings_data)
        top_3_stocks = top_5_stocks[:3]
        logging.info(f"Top 5 After Close by Market Cap: {top_5_stocks}")
        logging.info(f"Top 3 for Price Check: {top_3_stocks}")
        return top_3_stocks

    except Exception as e:
        logging.error(f"Error scraping earnings: {e}.")
        return []
    
    finally:
        driver.quit()