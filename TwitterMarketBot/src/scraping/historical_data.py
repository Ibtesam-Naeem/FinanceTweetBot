
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging
from scraping.earnings_tradingview import get_todays_stocks 

logging = setup_logging("YahooFinanceScraper")

def extract_market_cap(market_cap_text):
    """
    Converts the market cap text to a full number.
    """
    try:
        if 'T' in market_cap_text:
            return float(market_cap_text.replace('T', '')) * 1_000_000_000_000
        elif 'B' in market_cap_text:
            return float(market_cap_text.replace('B', '')) * 1_000_000_000
        elif 'M' in market_cap_text:
            return float(market_cap_text.replace('M', '')) * 1_000_000
        else:
            return None
    except Exception as e:
        logging.error(f"Error converting market cap: {e}")
        return None

def navigate_to_yahoo():
    """
    Navigates to Yahoo Finance pages and extracts data
    for each stock reporting earnings today
    """
    driver = chrome_options() 
    logging.info("WebDriver Initialized")

    todays_stocks = get_todays_stocks() 

    for stock in todays_stocks:
        try:
            driver.get(f"https://finance.yahoo.com/quote/{stock}/")
            logging.info(f"Navigated to {stock}'s YahooFinance page")

        except Exception as e:
            logging.error(f"Failed to intialize WebDriver: {e}.")
    
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            accept_button.click()
            logging.info("Accepted cookies.")

        except Exception as e:
            logging.info(f"No cookie popup.")

        try:
            market_cap_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Market Cap (intraday)')]/ancestor::li//fin-streamer[@data-field='marketCap']"))
            )
            market_cap_text = market_cap_elem.text
            logging.info(f"Market Cap (Raw): {market_cap_text}")

            market_cap_number = extract_market_cap(market_cap_text)
            if market_cap_number and market_cap_number > 10_000_000_000:
                formatted_market_cap = f"{market_cap_number:,.0f}"
                logging.info(f"Market Cap: {formatted_market_cap}")

                try:
                    statistics_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/key-statistics/')]"))
                    )
                    statistics_button.click()
                    logging.info("Clicked on 'Statistics' button.")
                    extract_statistics_page(driver)
                except Exception as e:
                    logging.error(f"Error clicking on 'Statistics' button: {e}")
            else:
                logging.info("Market cap is below $10 billion. Skipping Statistics page.")

        except Exception as e:
            logging.error(f"Error processing {stock}: {e}")  

def extract_statistics_page(driver):
    """
    Extracts 52-Week Low, 52-Week High, 52-Week Percentage Change,
    50-Day Moving Average, and 200-Day Moving Average from Yahoo Finance.
    """
    try:
        low = high = percentage = average_50 = average_200 = None

        stats_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        logging.info("Statistics table loaded successfully.")

        try:
            low_elem = stats_table.find_element(By.XPATH, ".//td[contains(text(), '52 Week Low')]/following-sibling::td")
            low = low_elem.text
            logging.info(f"52-Week Low: {low}")

        except Exception as e:
            logging.error(f"Error extracting 52-Week Low: {e}")

        try:
            high_elem = stats_table.find_element(By.XPATH, ".//td[contains(text(), '52 Week High')]/following-sibling::td")
            high = high_elem.text
            logging.info(f"52-Week High: {high}")

        except Exception as e:
            logging.error(f"Error extracting 52-Week High: {e}")

        try:
            percentage_elem = stats_table.find_element(By.XPATH, ".//td[contains(text(), '52 Week Range')]/following-sibling::td")
            percentage = percentage_elem.text
            logging.info(f"52-Week Percentage Change: {percentage}")

        except Exception as e:
            logging.error(f"Error extracting 52-Week Percentage Change: {e}")

        try:
            moving_average_elem = stats_table.find_element(By.XPATH, ".//td[contains(text(), '50-Day Moving Average')]/following-sibling::td")
            average_50 = moving_average_elem.text
            logging.info(f"50-Day Moving Average: {average_50}")

        except Exception as e:
            logging.error(f"Error extracting 50-Day Moving Average: {e}")

        try:
            moving_average_elem = stats_table.find_element(By.XPATH, ".//td[contains(text(), '200-Day Moving Average')]/following-sibling::td")
            average_200 = moving_average_elem.text
            logging.info(f"200-Day Moving Average: {average_200}")

        except Exception as e:
            logging.error(f"Error extracting 200-Day Moving Average: {e}")

        extracted_data = {
            "52_week_low": low,
            "52_week_high": high,
            "52_week_percentage": percentage,
            "50_day_moving_average": average_50,
            "200_day_moving_average": average_200
        }

        logging.info(f"Extracted Financial Highlights: {extracted_data}")
        return extracted_data

    except Exception as e:
        logging.error(f"Error extracting financial highlights: {e}")
        return None
    
if __name__ == "__main__":
    navigate_to_yahoo()
