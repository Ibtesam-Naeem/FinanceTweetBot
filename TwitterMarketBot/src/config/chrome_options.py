import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def chrome_options():
    """
    Configures and returns a Chrome 
    WebDriver instance 
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.binary_location = os.getenv("CHROME_BINARY_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    chrome_options.page_load_strategy = "eager"
    service = Service(executable_path='/usr/local/bin/chromedriver')
    
    return webdriver.Chrome(service=service, options=chrome_options)

