# Automated Earnings, Economic Events, and Market Updates Tweets

This project automates the process of tweeting about earnings reports, economic events, and market updates using **Tweepy** and **X API**. It fetches data from the **FinancialSuite-Backend** API, formats it into clean, readable tweets, and posts them automatically. The project is designed to be hosted on **AWS Lambda**, ensuring low-cost, efficient automation.

---

## **Architecture**

This Twitter bot is part of a larger system:

1. **FinancialSuite-Backend**: Handles all data scraping, processing, and storage
2. **FinancialSuite-TwitterBot**: Consumes the backend API and posts formatted tweets

This separation of concerns allows for:
- Centralized data collection and processing
- Multiple frontends/bots using the same data source
- Easier maintenance and updates
- Better error handling and monitoring

---

## **Features**

### **1. Daily Tweets**
- **Morning Updates (7 AM):**
  - **Earnings Calendar:**
    - Example:
      ```
      Major companies reporting earnings today after the bell:
      - $AAPL --->
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

### **7. AI-Powered Market Sentiment Analysis**
- **Machine Learning-based sentiment analysis of market news**
- **Scheduled tweets at 11:00 AM and 3:00 PM**
- **Features:**
  - Sentiment classification (positive, neutral, negative)
  - Market impact assessment
  - AI-generated market signals
- **Example:**
  ```
  📊 Market AI Analysis:

  🟢 S&P 500 reaches new all-time high as tech stocks surge

  AI Sentiment: Positive
  Market Signal: Moderately bullish signal

  Source: Market News
  Time: 2023-03-10 15:30:45

  #MarketAI #FinancialAnalysis #ML
  ```

---

## **Data Sources**
- **FinancialSuite-Backend API:**
  - Provides all market data through a unified API
  - Handles data collection, processing, and storage
  - Exposes endpoints for earnings, economic events, market movers, etc.

---

## **Project Workflow**

### **1. Daily Workflow**
- **Morning (7 AM):**
  1. Fetch earnings and economic data from the backend API
  2. Format the data into daily tweets
  3. Post tweets via **Tweepy**

- **After Market Close:**
  1. Fetch 52-week highs and lows from the backend API
  2. Format the data into tweets
  3. Post the tweets

### **2. Weekly Workflow (Sunday, 8 PM):**
1. Fetch earnings and economic events for the week from the backend API
2. Format the data into a weekly outlook tweet
3. Post the tweet

### **3. Real-Time Workflow:**
1. Fetch real-time earnings data from the backend API
2. Format and post the earnings tweet
3. Fetch stock price reaction data and post a reply tweet

---

## **Project Structure**

```
├── main.py                         # Centralized entry point for all functionality
├── models/                         # Directory for trained ML models
│   ├── market_sentiment_model.pkl  # Trained sentiment analysis model
│   ├── market_sentiment_vectorizer.pkl # TF-IDF vectorizer for sentiment analysis
├── logs/                           # Log files directory
├── src/
│   ├── config/
│   │   ├── api_client.py           # Handles API calls to the backend
│   │   ├── logger.py               # Logging configuration
│   ├── twitter/
│   │   ├── tweet_format.py         # Formats tweet content
│   ├── ml/
│   │   ├── __init__.py             # ML module initialization
│   │   ├── sentiment_analyzer.py   # Sentiment analysis using scikit-learn
│   │   ├── market_sentiment_tweet.py # Generates market sentiment tweets
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .env                            # Environment variables (gitignored)
├── .gitignore                      # Git ignore file
```

## **Centralized Approach**

The project uses a centralized approach with a single `main.py` file that serves as the entry point for all functionality:

1. **Setup Mode**: Creates necessary directories and downloads NLTK data
   ```bash
   python main.py --mode setup
   ```

2. **Train Mode**: Trains the sentiment analysis model with market-related text data
   ```bash
   python main.py --mode train
   ```

3. **Test Mode**: Tests the ML functionality by analyzing sample texts and generating a sample tweet
   ```bash
   python main.py --mode test
   ```

4. **Run Mode**: Runs the Twitter bot with scheduled tweets
   ```bash
   python main.py --mode run
   ```

5. **All Mode**: Runs all of the above in sequence
   ```bash
   python main.py --mode all
   # or simply
   python main.py
   ```

This centralized approach makes it easy to manage the project and ensures that all components work together seamlessly.

---

## **Hosting**

- **AWS Lambda:**
  - All workflows are deployed and hosted on AWS Lambda for efficient and low-cost automation.
- **AWS CloudWatch:**
  - Schedules daily and weekly workflows.
- **Environment Variables:**
  - API keys and sensitive credentials are securely managed using environment variables.

---

## **Technical Details**

### **Technologies Used**
- **Python 3.9+**
- **Tweepy**: Twitter API client
- **Schedule**: Task scheduling
- **Requests**: HTTP client for API calls
- **scikit-learn**: Machine learning library for sentiment analysis
- **NLTK**: Natural language processing for text preprocessing

---

## **Getting Started**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```

2. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`:
   ```env
   # Twitter API Credentials
   API_KEY=your_twitter_api_key
   API_SECRET=your_twitter_api_secret
   ACCESS_TOKEN=your_twitter_access_token
   ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   BEARER_TOKEN=your_twitter_bearer_token
   
   # Backend API Configuration
   BACKEND_URL=http://localhost:8000  # Change this to your backend URL
   ```

4. Run the setup to create necessary directories and download NLTK data:
   ```bash
   python main.py --mode setup
   ```

5. Train the sentiment analysis model:
   ```bash
   python main.py --mode train
   ```

6. Test the ML functionality:
   ```bash
   python main.py --mode test
   ```

7. Run the Twitter bot:
   ```bash
   python main.py --mode run
   ```

8. Or do all of the above in one command:
   ```bash
   python main.py --mode all
   # or simply
   python main.py
   ```

---

## **Dependencies**

The Twitter bot depends on the FinancialSuite-Backend API being available. Make sure the backend is running and accessible before starting the bot.

### **Required Backend Endpoints**

The Twitter bot expects the following endpoints to be available in the backend:

1. `/economic-events` - Economic calendar events
2. `/earnings` - Company earnings data
3. `/fear-greed` - Fear & Greed index
4. `/premarket` - Pre-market movers
5. `/market-data/52-week-highs` - 52-week high stocks
6. `/market-data/52-week-lows` - 52-week low stocks
7. `/market-data/all-time-highs` - All-time high stocks
8. `/market-data/gaps` - Gap stocks
9. `/market-data/daily-summary` - Daily market summary
10. `/market-data/weekly-summary` - Weekly market summary
11. `/market-data/trading-holidays` - Trading holidays

See `BACKEND_ENDPOINTS.md` for details on implementing these endpoints in the backend.

## **Future Improvements**
- Add sentiment analysis for earnings tweets.
- Include more granular stock price metrics (e.g., volume changes).
- Expand coverage to international markets.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for more details.
