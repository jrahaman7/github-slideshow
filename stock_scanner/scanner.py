import os
import time
import git
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

# Get the API key from an environment variable or prompt the user
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    API_KEY = input("Please enter your Alpha Vantage API key: ")

# List of tickers to scan
TICKERS = ["AAPL", "GOOG", "MSFT"]

def get_stock_data(ticker):
    """
    Fetches intraday and daily stock data for a given ticker.
    """
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    ti = TechIndicators(key=API_KEY, output_format='pandas')
    try:
        intraday_data, meta_data = ts.get_intraday(symbol=ticker, interval='60min', outputsize='full')
        daily_data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
        sma_50, meta_data = ti.get_sma(symbol=ticker, interval='daily', time_period=50, series_type='close')
        sma_200, meta_data = ti.get_sma(symbol=ticker, interval='daily', time_period=200, series_type='close')
        return intraday_data, daily_data, sma_50, sma_200
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None, None, None, None

def is_surging(data):
    """
    Checks if a stock is surging (price increase of 5% or more in 8 hours).
    This is based on the last 8 hourly data points.
    """
    if data is None or len(data) < 8:
        return False

    latest_price = data['4. close'].iloc[0]
    price_8_hours_ago = data['4. close'].iloc[7]

    price_change_percentage = ((latest_price - price_8_hours_ago) / price_8_hours_ago) * 100

    return price_change_percentage >= 5

def is_bullish(sma_50, sma_200):
    """
    Checks if a stock is bullish (Golden Cross: 50-day SMA > 200-day SMA).
    """
    if sma_50 is None or sma_200 is None:
        return False

    latest_sma_50 = sma_50['SMA'].iloc[0]
    latest_sma_200 = sma_200['SMA'].iloc[0]

    return latest_sma_50 > latest_sma_200

def main():
    """
    Main function to scan tickers and identify surging and bullish stocks.
    """
    # Clean up old files
    if os.path.exists("surging_stocks.txt"):
        os.remove("surging_stocks.txt")
    if os.path.exists("bullish_stocks.txt"):
        os.remove("bullish_stocks.txt")

    for i in range(8):
        print(f"--- Running scan {i+1}/8 ---")
        surging_stocks = []
        bullish_stocks = []
        for ticker in TICKERS:
            print(f"Scanning {ticker}...")
            intraday_data, daily_data, sma_50, sma_200 = get_stock_data(ticker)
            if is_surging(intraday_data):
                surging_stocks.append(ticker)
                print(f"{ticker} is surging!")
            if is_bullish(sma_50, sma_200):
                bullish_stocks.append(ticker)
                print(f"{ticker} is bullish!")

        with open("surging_stocks.txt", "a") as f:
            for ticker in surging_stocks:
                f.write(f"{ticker} - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        with open("bullish_stocks.txt", "a") as f:
            for ticker in bullish_stocks:
                f.write(f"{ticker} - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Commit and push the results to Git
        if len(surging_stocks) > 0 or len(bullish_stocks) > 0:
            try:
                repo = git.Repo(search_parent_directories=True)
                repo.index.add(["surging_stocks.txt", "bullish_stocks.txt"])
                repo.index.commit("Update stock lists")
                origin = repo.remote(name="origin")
                origin.push()
            except Exception as e:
                print(f"Error with Git operations: {e}")

        print("--- Scan complete. Waiting for the next run... ---")
        time.sleep(3600) # Sleep for 1 hour (3600 seconds)

if __name__ == "__main__":
    main()
