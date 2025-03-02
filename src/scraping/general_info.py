import json
from datetime import datetime, timedelta

def trading_holidays():
    """
    Checks if the stock market is open or
    closed tomorrow.
    """
    with open('trading_days.json', 'r') as file:
        holidays = json.load(file)

    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    holiday_info = next((holiday for holiday in holidays['2025'] if holiday['date'] == tomorrow_str), None)

    if holiday_info:
        return True, holiday_info['holiday']
    else:
        return False, None 
