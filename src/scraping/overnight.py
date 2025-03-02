import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging

logging = setup_logging("OvernightLogger")

STOCKS = ["GME", "CHWY"]

def scrape_robinhood():
    """
    Scrapes Robinhood for overnight prices (8 PM onwards)
    and logs stock price and percentage change.
    """
    try:
        driver = chrome_options() 
        stock_data = {}

        for stock in STOCKS:
            try:
                time.sleep(0.01) 
                url = f"https://robinhood.com/us/en/stocks/{stock}/"
                driver.get(url)

                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sdp-market-price"))
                )
                price = price_element.text.replace("Overnight", "").strip()

                price_change_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "sdp-price-chart-price-change"))
                )
                price_change = price_change_element.text.replace("Overnight", "").replace("Today", "").strip()

                stock_data[stock] = {
                    "price": price, 
                    "change": price_change
                    }
                
                logging.info(f"{stock} Price: ${price} | Change: {price_change}")
            
            except Exception as e:
                logging.error(f"Error scraping {stock}: {e}")

        driver.quit() 

        return stock_data

    except Exception as e:
        logging.error(f"Critical error in Robinhood scraper: {e}")

if __name__ == "__main__":
    stock_prices = scrape_robinhood()
    print(stock_prices) 
