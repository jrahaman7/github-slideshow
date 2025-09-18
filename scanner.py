import os
import time
from alpha_vantage.timeseries import TimeSeries

# Replace with your Alpha Vantage API key
API_KEY = "X9T7WY21N1FOZLTE"

# List of tickers to scan
TICKERS = ["AAPL", "GOOG", "MSFT"]

def get_stock_data(ticker):
    """
    Fetches intraday stock data for a given ticker.
    """
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    try:
        data, meta_data = ts.get_intraday(symbol=ticker, interval='60min', outputsize='full')
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def is_surging(data):
    """
    Checks if a stock is surging (price increase of 5% or more in 8 hours).
    """
    if data is None or len(data) < 8:
        return False

    latest_price = data['4. close'].iloc[0]
    price_8_hours_ago = data['4. close'].iloc[7]

    price_change_percentage = ((latest_price - price_8_hours_ago) / price_8_hours_ago) * 100

    return price_change_percentage >= 5

def is_bullish(data):
    """
    Checks if a stock is bullish (50-period SMA > 200-period SMA).
    This is a simplified check and requires more data than the current intraday fetch.
    For a proper implementation, we would need daily data.
    """
    if data is None:
        return False

    # This is a placeholder. A real implementation would need more historical data.
    # For now, we'll just return False to avoid false positives.
    return False

def main():
    """
    Main function to scan tickers and identify surging stocks.
    """
    for i in range(8):
        print(f"--- Running scan {i+1}/8 ---")
        surging_stocks = []
        for ticker in TICKERS:
            print(f"Scanning {ticker}...")
            data = get_stock_data(ticker)
            if is_surging(data):
                surging_stocks.append(ticker)
                print(f"{ticker} is surging!")

        with open("surging_stocks.txt", "w") as f:
            for ticker in surging_stocks:
                f.write(f"{ticker}\n")

        # Commit and push the results to Git
        if os.path.getsize("surging_stocks.txt") > 0:
            os.system("git add surging_stocks.txt")
            os.system('git commit -m "Update surging stocks list"')
            os.system("git push")

        print("--- Scan complete. Waiting for the next run... ---")
        time.sleep(3600) # Sleep for 1 hour (3600 seconds)

if __name__ == "__main__":
    main()
