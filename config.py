# config.py

# Define financial instruments and initial prices
INSTRUMENTS = ["NSE:ACC", "NSE:SBIN", "NSE:TCS", "NSE:INFY"]
INITIAL_PRICES = {
    "NSE:ACC": 100.0,
    "NSE:SBIN": 200.0,
    "NSE:TCS": 1500.0,
    "NSE:INFY": 800.0
}
LOG_FILE = "price_spikes.csv"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
