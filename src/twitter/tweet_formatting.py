# ---------------------------- EARNINGS REMINDER TWEETS ----------------------------
def premarket_earnings_tweet(earnings_list):
    """
    Formats the Pre-Market earnings tweet.
    """
    if not earnings_list:
        return None

    tweet = "Major companies reporting earnings TODAY BEFORE the bell:\n\n"

    for stock in earnings_list:
        tweet += (
            f"- ${stock['Ticker']} --->\n"
            f"  EPS estimate: {stock['EPS Estimate']}\n"
            f"  Revenue estimate: {stock['Revenue Forecast']}\n\n"
        )

    return tweet

def afterhrs_earnings_tweet(earnings_list):
    """
    Formats the After-Hours earnings tweet.
    """
    if not earnings_list:
        return None

    tweet = "Major companies reporting earnings TODAY AFTER the bell:\n\n"

    for stock in earnings_list:
        tweet += (
            f"- ${stock['Ticker']} --->\n"
            f"  EPS estimate: {stock['EPS Estimate']}\n"
            f"  Revenue estimate: {stock['Revenue Forecast']}\n\n"
        )

    return tweet

# ---------------------------- EARNINGS REPORTED TWEETS ----------------------------
def earnings_results(ticker, eps_estimate, reported_eps, revenue_estimate, reported_revenue):
    """
    Formats the tweet showing the earnings results with estimates vs reported.
    """
    tweet = (
        f"${ticker} HAS JUST REPORTED EARNINGS\n\n"
        f"EPS --->\n"
        f"  Estimate: ${eps_estimate}\n"
        f"  Reported: ${reported_eps}\n\n"
        f"Revenue --->\n"
        f"  Estimate: ${revenue_estimate}\n"
        f"  Reported: ${reported_revenue}"
    )

    return tweet

# ---------------------------- ECON REMINDER TWEETS ----------------------------
def get_country_flag(country):
    """
    Returns the appropriate flag emoji based on the country.
    """
    if country.lower() == "canada":
        return "🇨🇦"
    return "🇺🇸"

def econ_reminder_tomorrow(econ_list):
    """
    Formats the Economic Event tweet for TODAY.
    """
    if not econ_list:
        return None

    tweet = "Major Economic events to watch for TOMORROW:\n\n"

    for event in econ_list:
        flag = get_country_flag(event.get('Country', 'US'))
        time = event.get('Time', 'N/A')
        forecast = event.get('Forecast', 'N/A')
        prior = event.get('Prior', 'N/A')
        tweet += f"{flag} {event['Event']}\n"
        tweet += f"  Time: {time}\n"
        tweet += f"  Forecast: {forecast}\n"
        tweet += f"  Prior: {prior}\n\n"

    return tweet

def econ_reminder_weekly(econ_list):
    """
    Formats the Weekly Economic Event tweet.
    """
    if not econ_list:
        return None

    tweet = "Weekly Economic Calendar:\n\n"

    for event in econ_list:
        flag = get_country_flag(event.get('Country', 'US'))
        time = event.get('Time', 'N/A')
        forecast = event.get('Forecast', 'N/A')
        prior = event.get('Prior', 'N/A')
        date = event['Date'].split('T')[0]
        
        tweet += f"{flag} {event['Event']}\n"
        tweet += f"  Date: {date}\n"
        tweet += f"  Time: {time}\n"
        tweet += f"  Forecast: {forecast}\n"
        tweet += f"  Prior: {prior}\n\n"

    return tweet

# ---------------------------- PRE-MARKET MOVERS TWEETS ----------------------------
def pre_market_gainer(gainers_list):
    """
    Formats the Pre-Market Gainers tweet.
    """
    if not gainers_list:
        return None

    tweet = "Stocks rising in pre-market\n\n"

    for stock in gainers_list[:10]:
        tweet += f"- {stock['Ticker']} last up {stock['Pre-Market Change']}\n"

    return tweet

def pre_market_losers(losers_list):
    """
    Formats the Pre-Market Losers tweet.
    """
    if not losers_list:
        return None

    tweet = "Stocks dropping in pre-market\n\n"

    for stock in losers_list[:10]:
        tweet += f"- {stock['Ticker']} last down {stock['Pre-Market Change']}\n"

    return tweet

# ---------------------------- FEAR & GREED INDEX TWEETS ----------------------------
def fear_sentiment(greed_data):
    """
    Formats a tweet for the Fear & Greed Index.
    """
    if not greed_data:
        return None

    if isinstance(greed_data, list):
        if not greed_data:
            return None

        greed = greed_data[0]
    else:
        greed = greed_data

    category = greed.get("Category", "Unknown")
    fear_value = greed.get("Fear Value", "N/A")

    tweet = (
        "🚨 The Fear & Greed Index has just entered new territory! 🚨\n"
        f"Current Sentiment: {category}\n"
        f"Fear & Greed Score: {fear_value}\n\n"
        "How do you feel about the market? 📉📈"
    )

    return tweet

# ---------------------------- TRADING HOLIDAY TWEETS ----------------------------
def trading_holiday(closing_dates):
    """
    Formats the Stock Market Closing dates tweet.
    """
    if not closing_dates:
        return "Stock Market Open All Week"

    tweet = f"The Stock Market is closed tomorrow for {closing_dates}."

    return tweet

