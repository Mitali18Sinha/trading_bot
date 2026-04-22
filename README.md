# Binance Futures Testnet Trading Bot

A lightweight Python CLI tool for placing orders on the **Binance Futures Testnet (USDT-M)**. Supports Market, Limit, and Stop-Market orders with structured logging and clean error handling.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper (auth + HTTP)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # File + console logging setup
├── cli.py                 # CLI entry point (argparse)
├── logs/                  # Auto-created; log files written here
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Only `requests` is required — no third-party Binance SDK needed.

### 3. Create a Binance Futures Testnet account

- Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
- Register and log in
- Under **API Management**, generate an API key and secret

### 4. Set environment variables

On Mac/Linux:
```bash
export BINANCE_API_KEY=your_testnet_api_key
export BINANCE_API_SECRET=your_testnet_api_secret
```

On Windows (CMD):
```cmd
set BINANCE_API_KEY=your_testnet_api_key
set BINANCE_API_SECRET=your_testnet_api_secret
```

---

## How to Run

### Place a Market order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a Limit order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

### Place a Stop-Market order (Bonus)

```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_MARKET --quantity 0.001 --stop-price 50000
```

### Preview an order without placing it (Dry Run)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
```

Dry run prints the order summary and exits without hitting the API. Useful for validating inputs before placing a real order.

### View all options

```bash
python cli.py --help
```

---

## Example Output

### Market / Limit order

```
--- Order Request ----------------------------
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.001
----------------------------------------------

--- Order Response -----------------------------
  Order ID     : 13060639946
  Status       : NEW
  Executed Qty : 0.0000
  Avg Price    : 0.00
  Symbol       : BTCUSDT
  Side         : BUY
  Type         : MARKET
------------------------------------------------

 Order placed successfully.
```

### Dry Run

```
--- Order Request ----------------------------
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.001
----------------------------------------------

Dry run mode — order not placed.
```

---

## Logging

Logs are written to `logs/trading_bot_YYYYMMDD.log`. Each log entry captures:

- Timestamp and log level
- API request parameters (excluding signature)
- Full API response body
- Validation errors and exception details

Log level on console is `INFO`; the file captures full `DEBUG` output.

---

## Assumptions

- All orders are placed against **USDT-M perpetual futures** on the testnet.
- Credentials are provided via environment variables (not hardcoded).
- `timeInForce` defaults to `GTC` for Limit orders.
- Quantity precision must comply with the symbol's lot size filter on Binance; if you get a `-1111` filter error, try rounding your quantity (e.g., `0.001` instead of `0.0015`).
- Limit price must be within Binance's allowed range from current market price; extremely high prices like `999999` will be rejected with error `-4002`.
- The bot does not manage open positions or cancel existing orders — it is order-entry only.

---

## What I'd Improve in Production

- Poll order status after placement to confirm execution
- Check account balance before placing an order to prevent insufficient margin errors
- Add rate-limit handling with automatic retry and backoff
- Support multiple trading pairs in a single session

---

## Requirements

- Python 3.8+
- `requests >= 2.31.0`
