import os
import psycopg2
from dotenv import load_dotenv
from datetime import date 

load_dotenv()

DB_URL = os.getenv("DB_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL)

def store_earnings_data(data):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS earnings_reports (
            id SERIAL PRIMARY KEY,
            ticker TEXT NOT NULL,
            report_date DATE NOT NULL,
            eps_estimate TEXT,
            revenue_forecast TEXT,
            time TEXT,
            UNIQUE (ticker, report_date, time)
        )
    """)
    conn.commit()
    
    for record in data:
        cur.execute("""
            INSERT INTO earnings_reports (ticker, report_date, eps_estimate, revenue_forecast, time)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (ticker, report_date, time) DO UPDATE
            SET eps_estimate = EXCLUDED.eps_estimate,
                revenue_forecast = EXCLUDED.revenue_forecast,
                time = COALESCE(EXCLUDED.time, earnings_reports.time)
        """, (
            record["Ticker"],
            record["report_date"],
            record["EPS Estimate"],
            record["Revenue Forecast"],
            None if record["Time"] == "Unknown" else record["Time"]
        ))
    
    conn.commit()
    cur.close()
    conn.close()

def get_todays_earnings():
    """
    Fetches earnings data for today from the earnings_reports table.
    Returns a list of dictionaries matching the expected format.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    today = date.today()
    cur.execute("""
        SELECT ticker, report_date, eps_estimate, revenue_forecast, time
        FROM earnings_reports
        WHERE report_date = %s;
    """, (today,))
    
    rows = cur.fetchall()
    earnings_data = [
        {
            "Ticker": row[0],
            "report_date": row[1],  
            "EPS Estimate": row[2],
            "Revenue Forecast": row[3],
            "Time": row[4] if row[4] else "Unknown"
        }
        for row in rows
    ]
    
    cur.close()
    conn.close()
    return earnings_data

def store_economic_data(data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS economic_events (
            id SERIAL PRIMARY KEY,
            event TEXT NOT NULL,
            date DATE NOT NULL,
            UNIQUE (event, date)
        )
    """)
    conn.commit()

    for record in data:
        cur.execute("""
            INSERT INTO economic_events (event, date)
            VALUES (%s, %s)
            ON CONFLICT (event, date) DO NOTHING;
        """, (record["event"], record["date"]))

    conn.commit()
    cur.close()
    conn.close()

def store_trading_holidays(holidays):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS trading_holidays (
            id SERIAL PRIMARY KEY,
            holiday_date DATE UNIQUE NOT NULL,
            holiday_name TEXT NOT NULL,
            early_close BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()

    for holiday in holidays:
        cur.execute("""
            INSERT INTO trading_holidays (holiday_date, holiday_name, early_close)
            VALUES (%s, %s, %s)
            ON CONFLICT (holiday_date) DO NOTHING;
        """, (
            holiday["date"], 
            holiday["holiday"], 
            holiday.get("early_close", False)
        ))

    conn.commit()
    cur.close()
    conn.close()

def store_fear_greed_index(fear_value, category):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fear_greed_index (
            id SERIAL PRIMARY KEY,
            date DATE UNIQUE DEFAULT CURRENT_DATE,
            fear_value INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    """)
    
    cur.execute("""
        INSERT INTO fear_greed_index (date, fear_value, category)
        VALUES (CURRENT_DATE, %s, %s)
        ON CONFLICT (date) DO UPDATE
        SET fear_value = EXCLUDED.fear_value,
            category = EXCLUDED.category
    """, (fear_value, category))
    
    conn.commit()
    cur.close()
    conn.close()

def get_latest_fear_greed():
    """
    Retrieves the most recent Fear & Greed Index.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT fear_value, category FROM fear_greed_index ORDER BY date DESC LIMIT 1;")
    latest_data = cur.fetchone()

    cur.close()
    conn.close()

    return latest_data if latest_data else (None, None) 

def get_sp500_tickers():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT ticker FROM sp500_tickers;")
    tickers = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return tickers

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