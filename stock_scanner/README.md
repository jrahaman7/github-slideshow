# Stock Scanner

This application scans a list of stock tickers for surging and bullish signals.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Navigate to the application directory:**
    ```bash
    cd stock_scanner
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the Alpha Vantage API key:**
    Set the `ALPHA_VANTAGE_API_KEY` environment variable to your Alpha Vantage API key.
    ```bash
    export ALPHA_VANTAGE_API_KEY="YOUR_API_KEY"
    ```

## Usage

To run the scanner, execute the `scanner.py` script from within the `stock_scanner` directory:
```bash
python scanner.py
```

The script will run for 8 hours, scanning the tickers every hour. The results will be saved in `surging_stocks.txt` and `bullish_stocks.txt`, and will be committed and pushed to the Git repository.
