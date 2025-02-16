import json
import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
from config.logger import setup_logging

logging = setup_logging("SentimentLogger")
driver = chrome_options()

LAST_CATEGORY_FILE = "last_fear_category.json"

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

def get_last_fear_category():
    """
    Reads the last stored fear sentiment
    category, it will create one if none exists
    """
    if not os.path.exists(LAST_CATEGORY_FILE):
        save_fear_category("Unknown")
    
    with open(LAST_CATEGORY_FILE, "r") as f:
        return json.load(f).get("category", "Unknown") 

def save_fear_category(category):
    """
    Saves the new fear sentiment category.
    """
    with open(LAST_CATEGORY_FILE, "w") as f:
        json.dump({"category": category}, f)

def fear_index():
    """
    Scrapes the Fear & Greed Index
    and returns the data
    """
    try:
        driver.get("https://www.cnn.com/markets/fear-and-greed")    
        logging.info("Navigated to Fear & Greed Index")

        results = []

        chart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'dial-number-value')]")
        ))

        time.sleep(2)

        fear_value = chart.text
        category = get_fear_category(fear_value)
        last_category = get_last_fear_category()

        logging.info(f"Fear Value: {fear_value} - Category: {category}")

        if last_category != category:
            logging.info(f"New sentiment category detected! {last_category} has changed to {category}")
            save_fear_category(category)
            
            results.append({
                "Fear Value": fear_value,
                "Category": category,
            })
            return results
        else:
            logging.info(f"No change in sentiment. Current: {category}")
            return []

    except Exception as e:
        logging.error(f"Unable to locate fear value: {e}")
        return []