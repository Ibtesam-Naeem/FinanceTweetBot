import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging

logging  = setup_logging("EconScraper")

def open_earnings_calendar():
    """
    Navigates to the Trading Views
    USDCAD Economic Calendar page.
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
    Clicks the Importance filter button
    and then click on "Today"
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

def day(driver, option):
    """
    Selects the date given the scraping
    option: 'Tomorrow' or 'This Week'.
    """
    try:
        logging.info(f"Clicking on '{option}' option.")

        option_xpath = {
            "Tomorrow": '//*[@id="Tomorrow"]/span[1]/span',
            "This Week": '//*[@id="This week"]/span[1]/span'
        }

        if option not in option_xpath:
            logging.error(f"Invalid option: {option}")
            return

        button = driver.find_element(By.XPATH, option_xpath[option])
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        
        time.sleep(2)  
        
        driver.execute_script("arguments[0].click();", button)

        logging.info(f"'{option}' button clicked successfully.")

    except Exception as e:
        logging.error(f"Failed to click '{option}' button: {e}")

def scrape_economics_data(driver):
    """
    Extracts the Economic Event data from Trading View.
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

        econ_data.append({"Event": event_name})

    return econ_data
