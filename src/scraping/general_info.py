from config.db_manager import get_db_connection

def trading_holidays():
    """
    Fetches trading holidays from the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT holiday_date, holiday_name, early_close FROM trading_holidays;")
    holidays = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "date": holiday[0],
            "name": holiday[1],
            "early_close": holiday[2]
        }
        for holiday in holidays
    ]
