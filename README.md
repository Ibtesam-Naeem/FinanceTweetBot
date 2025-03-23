# FinancialSuite TwitterBot
### Automated Earnings, Economic Events, and Market Update Tweets

This project automates the process of tweeting about **earnings reports**, **economic events**, and **market updates** using **Tweepy** and the **Twitter/X API**. It fetches real-time and historical data from **FinancialSuite-Backend**, **Polygon API**, and **SEC API**, formats it into clean, informative tweets, and posts them automatically.

The bot runs on a scheduled system and continuously monitors **real-time earnings reports** via the SEC API to deliver timely tweets as soon as earnings are released.

---

## 🌐 Architecture

This Twitter bot is part of the **FinancialSuite Ecosystem**, designed for **modularity**, **scalability**, and **automation**.

```
FinancialSuite Ecosystem
├── FinancialSuite-Backend: Collects & processes financial data
├── FinancialSuite-TwitterBot: Formats and tweets the data automatically
```

---

## Features

### 1. Scheduled Tweets

#### 🕖 Pre-Market Earnings Reminder (7 AM)
Tweets a list of major companies reporting earnings **before** the market opens.

**Example Tweet:**
```
Major companies reporting earnings TODAY BEFORE the bell:

- $TSLA --->
  EPS estimate: $1.20
  Revenue estimate: $25B

- $GME --->
  EPS estimate: $-0.15
  Revenue estimate: $1.3B
```

---

#### 🕛 After-Hours Earnings Reminder (12 PM)
Tweets major companies reporting earnings **after** the bell.

**Example Tweet:**
```
Major companies reporting earnings TODAY AFTER the bell:

- $NVDA --->
  EPS estimate: $4.50
  Revenue estimate: $22B

- $NFLX --->
  EPS estimate: $2.80
  Revenue estimate: $8.5B
```

---

#### 📅 Weekly Economic & Earnings Outlook (Sunday, 8 PM)
Posts the full week's **earnings and economic calendar**.

**Example Tweet:**
```
📅 WEEKLY EARNINGS & ECONOMIC OUTLOOK 📅

🔸 Major Earnings Reports This Week:
- $AAPL ---> EPS: $1.82 | Revenue: $100B
- $MSFT ---> EPS: $2.80 | Revenue: $56B

🔸 Major Economic Events:
- FOMC Rate Decision ---> Forecast: 5.5%
- GDP (Q1) ---> Estimate: 3.5%
- Non-Farm Payrolls ---> Estimate: +250K
```

---

#### 📉 Trading Holidays Notification (8 PM)
Alerts users to upcoming **market closures**.

**Example Tweet:**
```
📢 Heads up!

The US Stock Market will be CLOSED tomorrow for Presidents Day 🇺🇸
```

---

#### 😱 Fear & Greed Index (7 PM)
Posts the current **Fear & Greed index** sentiment.

**Example Tweet:**
```
🚨 The Fear & Greed Index has just entered new territory! 🚨

Current Sentiment: EXTREME GREED
Fear & Greed Score: 88/100

How do you feel about the market? 📉📈
```

---

#### 🗓️ Daily Economic Events (10 PM)
Tweets **economic events** scheduled for tomorrow.

**Example Tweet:**
```
Major Economic events to watch for TOMORROW:

- GDP Report ---> Estimate: 3.5%, Prior: 3.2% (8:30 AM EST)
- Jobless Claims ---> Estimate: 210K (8:30 AM EST)
```

---

### 2. Real-Time SEC Earnings Reports
Continuously monitors the **SEC API** for **real-time 10-Q filings**. Tweets earnings as soon as they are reported.

**Example Tweet (Earnings Results):**
```
$TSLA HAS JUST REPORTED EARNINGS 🚨

EPS --->
  Estimate: $1.20
  Reported: $1.30 ✅ BEAT

Revenue --->
  Estimate: $25B
  Reported: $26.2B ✅ BEAT

Guidance: Revenue expected at $27B next quarter!
```

---

### 3. Polygon Financial Threads (8 PM)
Posts **threads** showing historical revenue, net income, and EPS from Polygon.io for top stocks.

**Example Tweet Thread:**

**Thread 1: Revenue**
```
$TSLA QUARTERLY REVENUE (Last 8 Quarters)

2023 Q4: $26.2B
2023 Q3: $25.0B
2023 Q2: $24.1B
2023 Q1: $23.3B
2022 Q4: $22.9B
2022 Q3: $21.8B
2022 Q2: $19.6B
2022 Q1: $18.7B
```

**Thread 2: Net Income**
```
$TSLA NET INCOME (Last 8 Quarters)

2023 Q4: $3.2B
2023 Q3: $3.0B
2023 Q2: $2.8B
2023 Q1: $2.5B
2022 Q4: $2.4B
2022 Q3: $2.3B
2022 Q2: $2.0B
2022 Q1: $1.9B
```

**Thread 3: EPS (Basic)**
```
$TSLA EPS (Basic, Last 8 Quarters)

2023 Q4: $1.30
2023 Q3: $1.20
2023 Q2: $1.10
2023 Q1: $1.00
2022 Q4: $0.90
2022 Q3: $0.85
2022 Q2: $0.75
2022 Q1: $0.70
```

---

## 🗂️ Project Workflow

### 🕖 Daily Schedule:
| Time     | Task                                      |
|----------|-------------------------------------------|
| 7:00 AM  | Pre-Market Earnings Reminder Tweet        |
| 12:00 PM | After-Hours Earnings Reminder Tweet       |
| 7:00 PM  | Fear & Greed Index Tweet                  |
| 8:00 PM  | Trading Holiday Notification Tweet        |
| 10:00 PM | Daily Economic Events Tweet               |
| 8:00 PM  | Polygon Financial Threads                 |

### 🕗 Weekly (Sunday)
| Time     | Task                                      |
|----------|-------------------------------------------|
| 8:00 PM  | Weekly Earnings & Economic Outlook Tweet  |

### 🔄 Real-Time Continuous Monitoring
| Task                                           |
|------------------------------------------------|
| Monitor SEC filings (10-Q) and tweet earnings reports immediately. |

---

## 🔗 Data Sources

- **FinancialSuite-Backend API**
- **Polygon.io API**
- **SEC.gov API**

---

## 🏗️ Project Structure

```
src/
├── config/
│   ├── backend_api.py
│   ├── logger.py
│   ├── twitter_client.py
├── data/
│   ├── polygon_financials.py
│   ├── sec_results.py
├── twitter/
│   ├── tweet_formatting.py
├── utils/
│   ├── helpers.py
├── main.py
```

---

## ⚙️ Technologies Used

- **API Clients:** `requests`
- **Twitter API:** `tweepy`
- **Scheduling:** `schedule`
- **Real-Time Earnings Monitoring:** `SEC API`
- **Financial Data Threads:** `Polygon API`
- **Environment Management:** `dotenv`
- **Logging:** `logging`
