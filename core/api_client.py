import requests
import os
import logging

logger = logging.getLogger(__name__)

# Pulls stock price data for a given symbol using a market API (mockable for testing)
def get_stock_data(symbol):
    try:
        api_url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        result = data["quoteResponse"]["result"][0]
        return result["regularMarketPrice"]
    except Exception as e:
        logger.error(f"[Stock API Error] Could not retrieve data for {symbol}: {e}")
        return None
