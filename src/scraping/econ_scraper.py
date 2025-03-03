import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging
from config.db_manager import store_economic_data  
logging  = setup_logging("EconScraper")

def open_economic_calendar():
    """
    Navigates to the Trading View USDCAD Economic Calendar page.
    """
    try:
        driver = chrome_options()
        driver.set_window_size(1920, 1080)

        logging.info("Initializing WebDriver and opening economic calendar page.")

        driver.get("https://www.tradingview.com/symbols/USDCAD/economic-calendar/?exchange=FX_IDC")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@data-name, 'economic-calendar-item')]"))
        )

        logging.info("Economic calendar page loaded successfully.")
        return driver

    except Exception as e:
        logging.error(f"Failed to open economic calendar: {e}")
        return None

def click_importance(driver):
    """
    Clicks the Importance filter button.
    """
    try:
        logging.info("Finding the High Importance button.")

        importance_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="js-category-content"]/div[2]/div/section/div/div[2]/div/div/div/div[1]/div[1]/button/span[2]/span[1]'))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", importance_button)
        time.sleep(2)
        
        driver.execute_script("arguments[0].click();", importance_button)
        
        logging.info("Importance button clicked successfully.")

    except Exception as e:
        logging.error(f"Failed to click Importance button: {e}")

def select_timeframe(driver, timeframe):
    """
    Selects the specified timeframe (e.g., 'Tomorrow', 'This Week') on the economic calendar.
    """
    try:
        logging.info(f"Selecting timeframe: {timeframe}")

        timeframe_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{timeframe}')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", timeframe_button)
        time.sleep(1)
        
        driver.execute_script("arguments[0].click();", timeframe_button)
        logging.info(f"Timeframe '{timeframe}' selected successfully.")
        
    except Exception as e:
        logging.error(f"Failed to select timeframe '{timeframe}': {e}")

def scrape_economic_data(driver):
    """
    Extracts the Economic Event data from TradingView.
    """
    logging.info("Waiting for the economic calendar to load.")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@data-name, 'economic-calendar-item')]"))
        )
        
    except Exception:
        logging.warning("No economic calendar data available. Skipping scrape.")
        return []  

    rows = driver.find_elements(By.XPATH, "//div[contains(@data-name, 'economic-calendar-item')]")

    if not rows:
        logging.warning("No economic calendar rows found. Skipping.")
        return []

    econ_data = []

    for row in rows:
        try:
            event_element = row.find_element(By.XPATH, ".//span[contains(@class, 'titleText')]")
            event_name = event_element.text.strip()
        except Exception:
            event_name = "N/A"

        econ_data.append({
            "event": event_name,
            "date": datetime.datetime.now().date()
        })

    return econ_data

def scrape_and_store_economic_data():
    """
    Scrapes today's economic events and stores them in the database.
    """
    driver = open_economic_calendar()
    if not driver:
        logging.error("WebDriver initialization failed.")
        return []

    try:
        economic_data = scrape_economic_data(driver)

        if economic_data:
            store_economic_data(economic_data)
            logging.info(f"Successfully stored {len(economic_data)} economic events in the database.")

        return economic_data

    except Exception as e:
        logging.error(f"Error scraping economic data: {e}.")
        return []
    
    finally:
        driver.quit()