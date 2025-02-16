import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options 
from config.logger import setup_logging
import time

logging = setup_logging("SentimentLogger")

driver = chrome_options()

def get_fear_category(fear_value):
    """
    Returns the Fear & Greed category based on the given value.
    """
    fear_value = int(fear_value)

    if 0 <= fear_value <= 25:
        return "Extreme Fear"
    elif 26 <= fear_value <= 44:
        return "Fear"
    elif 45 <= fear_value <= 55:
        return "Neutral"
    elif 56 <= fear_value <= 74:
        return "Greed"
    elif 75 <= fear_value <= 100:
        return "Extreme Greed"
    else:
        return "Unknown"
    
def fear_index():
    """
    Gets the value of the Fear & Greed
    Index
    """
    try:
        driver.get("https://www.cnn.com/markets/fear-and-greed")    
        logging.info("Navigated to Fear & Greed Index")

        results = []

        chart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'dial-number-value')]"))
        )

        time.sleep()

        fear_value = chart.text
        category = get_fear_category(fear_value)

        logging.info(f"Fear Value: {fear_value} - Category: {category}")
        results.append ({
            "Fear Value": fear_value,
            "Category": category,
        })
        return results
    
    except Exception as e:
        logging.error(f"Unable to locate fear value: {e}")
