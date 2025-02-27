def daily_premkt_earnings_tweet(earnings_list):
    """
    Formats the Pre-Market earnings reminder tweet.
    """
    if not earnings_list:
        return "No major earnings reports scheduled for today before the bell."

    tweet = "Major companies reporting earnings TODAY BEFORE the bell:\n\n"

    for stock in earnings_list:
        tweet += f"- ${stock['Ticker']} --->\n"
        tweet += f"  EPS estimate: {stock['EPS Estimate']}\n"
        tweet += f"  Revenue estimate: {stock['Revenue Forecast']}\n\n"

    return tweet.strip()

def daily_afterhrs_earnings_tweet(earnings_list):
    """
    Formats the After-Market earnings reminder tweet.
    """
    if not earnings_list:
        return "No major earnings reports scheduled for today after the bell."

    tweet = "Major companies reporting earnings TODAY AFTER the bell:\n\n"

    for stock in earnings_list:
        tweet += f"- ${stock['Ticker']} --->\n"
        tweet += f"  EPS estimate: {stock['EPS Estimate']}\n"
        tweet += f"  Revenue estimate: {stock['Revenue Forecast']}\n\n"

    return tweet.strip()

def econ_reminder_tomorrow(econ_list):
    """
    Formats the economic event reminder tweet for TOMORROW.
    """
    if not econ_list:
        return "No major economic events scheduled for tomorrow."

    tweet = "Major economic events TOMORROW:\n\n"

    for event in econ_list:
        tweet += f"- {event['Event']}\n"

    return tweet.strip()

def econ_reminder_weekly(econ_list):
    """
    Formats the economic event reminder tweet for THIS WEEK.
    """
    if not econ_list:
        return "No major economic events scheduled for this week."

    tweet = "Major economic events THIS WEEK:\n\n"

    for event in econ_list:
        tweet += f"- {event['Event']}\n"

    return tweet.strip()

def pre_market_gainer(gainers_list):
    """
    Formats the Pre-Market Gainers tweet.
    """
    if not gainers_list:
        return "No significant pre-market gainers today."

    tweet = "Stocks rising in pre-market\n\n"

    for stock in gainers_list[:10]:
        tweet += f"- {stock['Ticker']} last up {stock['Pre-Market Change']}\n"

    return tweet.strip()

def pre_market_losers(losers_list):
    """
    Formats the Pre-Market Losers tweet.
    """
    if not losers_list:
        return "No significant pre-market losers today."

    tweet = "Stocks dropping in pre-market\n\n"

    for stock in losers_list[:10]:
        tweet += f"- {stock['Ticker']} last down {stock['Pre-Market Change']}\n"

    return tweet.strip()

def week_high_52(high_list):
    """
    Formats the 52-Week Highs tweet.
    """
    if not high_list:
        return "No stocks hitting new 52-week highs today."

    tweet = "All these stocks hit a 52 WEEK HIGH at some point today\n\n"

    for stock in high_list[:10]:
        tweet += f"- {stock['Ticker']}\n"

    return tweet.strip()

def week_low_52(low_list):
    """
    Formats the 52-Week Lows tweet.
    """
    if not low_list:
        return "No stocks hitting new 52-week lows today."

    tweet = "All these stocks hit a 52 WEEK LOW at some point today\n\n"

    for stock in low_list[:10]:
        tweet += f"- {stock['Ticker']}\n"

    return tweet.strip()

def all_time_high(high_list):
    """
    Formats the All-Time Highs tweet.
    """
    if not high_list:
        return "No stocks reaching all-time highs today."

    tweet = "All these stocks hit ALL TIME HIGHS at some point today\n\n"

    for stock in high_list[:10]:
        tweet += f"- {stock['Ticker']}\n"

    return tweet.strip()

def all_time_low(low_list):
    """
    Formats the All-Time Lows tweet.
    """
    if not low_list:
        return "No stocks reaching all-time lows today."

    tweet = "All these stocks hit ALL TIME LOWS at some point today\n\n"

    for stock in low_list[:10]:
        tweet += f"- {stock['Ticker']}\n"
     
    return tweet.strip()

def pre_market_gap(gap_list):
    """
    Fromats the pre-market Gap tweet
    """
    if not gap_list:
        return "No stocks gapping today."
    
    tweet = "Stocks gapping up:"

    for stock in gap_list[:10]:
        tweet += f"- {stock['Ticker']} gapping up {stock['Pre-Market Change']}"

    return tweet.strip()

def kitty_posted(meme_list):
    """
    Formats a tweet when Roaring Kitty posts,
    displaying meme stock movements.
    """
    if not meme_list:
        return "No memes today"

    tweet = "ROARING KITTY HAS RETURNED\n"
    tweet += "MEME STOCKS ARE MOVINGGGGG\n\n"

    for stock in meme_list:
        tweet += f"${stock['ticker']} IS UP {stock['price_change']}% IN OVERNIGHT TRADING!!!\n"

    tweet += "\nWHO HERE STILL GOT DIAMONDS HANDS???"

    return tweet.strip()

def fear_sentiment(greed_list):
    """
    Formats a tweet for the Fear & Greed Index.
    """
    if not greed_list or len(greed_list) == 0:
        return "Not available"

    greed = greed_list[0]
    category = greed_list.get("Category", "Unknown")
    fear_value = greed_list.get("Fear Value", "N/A")

    tweet = "🚨 The Fear & Greed Index has just entered new territory! 🚨\n"
    tweet += f"Current Sentiment: {category}\n"
    tweet += f"Fear & Greed Score: {fear_value}\n\n"
    tweet += "How do you feel about the market? 📉📈"

    return tweet.strip()

def daily_market_summary(market_data):
    """
    Formats a tweet for the daily closing
    prices of S&P 500 and Dow Jones.
    """
    if not market_data:
        return "Market data unavailable for today."

    sp500 = market_data.get("S&P 500", {})
    dow = market_data.get("Dow Jones", {})

    tweet = "As of closing, the S&P 500 finished "
    tweet += f"{sp500.get('Direction', 'unchanged')} {sp500.get('Percent Change', 'N/A')}% at ${sp500.get('Close', 'N/A')}.\n"
    tweet += f"The Dow Jones ended {dow.get('Direction', 'unchanged')} {dow.get('Percent Change', 'N/A')}% at ${dow.get('Close', 'N/A')}."

    return tweet.strip()

def weekly_market_summary(weekly_data):
    """
    Formats a tweet for the weekly closing
    summary of S&P 500 and Dow Jones.
    """
    if not weekly_data:
        return "Weekly market data unavailable."

    sp500 = weekly_data.get("S&P 500", {})
    dow = weekly_data.get("Dow Jones", {})

    tweet = "For the week, the S&P 500 moved "
    tweet += f"{sp500.get('Weekly Direction', 'unchanged')} {sp500.get('Weekly Percent Change', 'N/A')}%, closing at ${sp500.get('Friday Close', 'N/A')}.\n"
    tweet += f"The Dow Jones finished the week {dow.get('Weekly Direction', 'unchanged')} {dow.get('Weekly Percent Change', 'N/A')}%, ending at ${dow.get('Friday Close', 'N/A')}."

    return tweet.strip()

def closures(closing_dates):
    """
    Formats the Stock Market Closing dates tweet.
    """
    if not closing_dates:
        return "Stock Market Open All Week"
    
    tweet = f"The Stock Market is closed tomorrow for {closing_dates}."

    return tweet.strip()

