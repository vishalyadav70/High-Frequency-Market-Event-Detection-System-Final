# spike_detector.py

import csv
from datetime import datetime
import pytz
import json
from config import INSTRUMENTS, INITIAL_PRICES, LOG_FILE

# Initialize price history
price_history = {instrument: INITIAL_PRICES[instrument] for instrument in INSTRUMENTS}

def detect_spikes(tick):
    """Detect price spikes and log them if detected."""
    now = datetime.now(pytz.timezone('Asia/Kolkata'))  # IST timezone
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S.%f")[:-3]
    
    for instrument, new_price in tick.items():
        old_price = price_history[instrument]
        if abs(new_price - old_price) / old_price > 0.10:
            log_spike(instrument, old_price, new_price, date_str, time_str)
        price_history[instrument] = new_price

def log_spike(instrument, old_price, new_price, date, time):
    """Log spike details to a CSV file."""
    try:
        with open(LOG_FILE, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([instrument, old_price, new_price, f"{date} {time}"])
    except IOError as e:
        print(f"Error writing to log file: {e}")
