# Automated Earnings, Economic Events, and Market Updates Tweets

This project automates the process of tweeting about earnings reports, economic events, and market updates using **Tweepy** and **X API**. It scrapes data from **TradingView** and **SEC EDGAR**, formats it into clean, readable tweets, and posts them automatically. The project is hosted on **AWS Lambda**, ensuring low-cost, efficient automation.

---

## **Features**

### **1. Daily Tweets**
- **Morning Updates (7 AM):**
  - **Earnings Calendar:**
    - Example:
      ```
      Major companies reporting earnings today after the bell:
      - $AAPL --->
        EPS estimate: $1.82  
        Revenue estimate: $100B  
      ```
  - **Economic Events:**
    - Example:
      ```
      Major economic events today:
      - GDP ---> Estimate: 3.5%, Prior: 3.2% (9:30 AM EST)  
      ```

- **After Market Close Updates:**
  - **52-Week Highs:**
    - Example:
      ```
      At some point today, all these stocks hit a new 52-week high:
      - $AAPL - Apple  
      - $MSFT - Microsoft  
      ```
  - **52-Week Lows:**
    - Example:
      ```
      At some point today, all these stocks hit a new 52-week low:
      - $NFLX - Netflix  
      - $TSLA - Tesla  
      ```

---

### **2. Weekly Tweets (Sunday, 8 PM)**
- **Weekly Outlook:**
  - **Top 10 Earnings for the Week:**
    - Example:
      ```
      Major companies reporting earnings this week:
      - $MSFT --->
        EPS estimate: $2.85  
        Revenue estimate: $54B  

      - $AAPL --->
        EPS estimate: $1.82  
        Revenue estimate: $100B  
      ```
  - **Economic Events:**
    - Example:
      ```
      Major economic events this week:
      - GDP ---> Estimate: 3.5%, Prior: 3.2%  
      - FOMC Rate Decision ---> Forecast: 5.5%, Prior: 5.25%  
      ```

---

### **3. Real-Time Earnings Tweets**
- **Earnings Reports:**
  - Example:
    ```
    $AAPL has just reported its Q3 earnings:

    EPS ---> Estimate: $1.82  
    Reported: $1.95 ✅ BEAT  

    Revenue ---> Estimate: $100B  
    Reported: $97B ❌ MISS  

    Guidance for the next quarter:  
    Revenue expected at $110B (higher than analyst expectations).  
    ```

- **Stock Price Reaction Tweets:**
  - Example:
    ```
    $AAPL stock has dropped $14 (4%) in reaction to the news.  
    Current price: $310 (as of 4:05 PM EST).  
    ```

---

## **Data Sources**
- **TradingView:**
  - Scrapes the **earnings calendar**, **economic calendar**, and **52-week highs/lows**.
- **SEC EDGAR:**
  - Scrapes detailed earnings reports (EPS, revenue).
- **Stock Price APIs:**
  - Fetches real-time stock prices for **52-week highs/lows** and **price reactions**.

---

## **Project Workflow**

### **1. Daily Workflow**
- **Morning (7 AM):**
  1. Scrape earnings and economic calendars from **TradingView**.
  2. Format the data into daily tweets.
  3. Post tweets via **Tweepy**.

- **After Market Close:**
  1. Scrape daily 52-week highs and lows from **TradingView**.
  2. Format the data into a single tweet.
  3. Post the tweet.

### **2. Weekly Workflow (Sunday, 8 PM):**
1. Scrape top 10 earnings and key economic events for the week from **TradingView**.
2. Format the data into a weekly outlook tweet.
3. Post the tweet.

### **3. Real-Time Workflow:**
1. Monitor **SEC EDGAR** for real-time earnings filings.
2. Scrape and process the earnings report.
3. Format and post the earnings tweet.
4. Fetch stock price reaction and post a reply tweet.

---

## **Project Structure**
```
project/
├── data/
│   ├── earnings_calendar.json       # Cached daily/weekly earnings calendar.
│   ├── econ_calendar.json           # Cached economic calendar events.
│   ├── 52_week_highs_lows.json      # Cached data of daily 52-week highs and lows.
├── src/
│   ├── scraper/
│   │   ├── tradingview_scraper.py   # Scrapes TradingView data.
│   │   ├── sec_edgar_scraper.py     # Scrapes SEC EDGAR filings.
│   │   ├── stock_price_scraper.py   # Fetches real-time stock prices.
│   │   ├── 52_week_scraper.py       # Scrapes 52-week highs/lows.
│   ├── tweet/
│   │   ├── tweet_formatter.py       # Formats tweet content.
│   │   ├── tweet_scheduler.py       # Schedules and posts tweets.
│   │   ├── tweepy_client.py         # Handles Tweepy interactions.
│   ├── main.py                      # Orchestrates workflows.
├── config/
│   ├── settings.py                  # Configuration for APIs and schedules.
├── tests/
│   ├── test_scraper.py              # Unit tests for scrapers.
│   ├── test_tweet_formatter.py      # Unit tests for formatting.
├── requirements.txt                 # Python dependencies.
├── README.md                        # Project documentation.
├── .env                             # Environment variables (gitignored).
├── .gitignore                       # Git ignore file.
```

---

## **Hosting**

- **AWS Lambda:**
  - All workflows are deployed and hosted on AWS Lambda for efficient and low-cost automation.
- **AWS CloudWatch:**
  - Schedules daily and weekly workflows.
- **Environment Variables:**
  - API keys and sensitive credentials are securely managed using environment variables.

---

## **Technologies Used**

- **Data Scraping:** `requests`, `beautifulsoup4`, `selenium`
- **Twitter API:** `tweepy`
- **Hosting and Scheduling:** `AWS Lambda`, `AWS CloudWatch`
- **Environment Management:** `python-dotenv`

---

## **Getting Started**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   ```env
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   ...
   ```
4. Deploy to AWS Lambda:
   - Package the project and upload it to AWS Lambda.
   - Configure triggers using AWS CloudWatch.

---

## **Future Improvements**
- Add sentiment analysis for earnings tweets.
- Include more granular stock price metrics (e.g., volume changes).
- Expand coverage to international markets.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for more details.
