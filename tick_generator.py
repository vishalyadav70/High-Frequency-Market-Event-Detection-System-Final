# tick_generator.py

import random
import time
import json
import redis
from config import INSTRUMENTS, INITIAL_PRICES, REDIS_HOST, REDIS_PORT, REDIS_DB

# Redis client setup
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Initialize price history
price_history = {instrument: INITIAL_PRICES[instrument] for instrument in INSTRUMENTS}

def generate_and_enqueue_ticks():
    """Generate ticks and enqueue them into Redis."""
    while True:
        tick = {instrument: round(random.uniform(price_history[instrument] * 0.95, price_history[instrument] * 1.05), 2)
                for instrument in INSTRUMENTS}
        redis_client.lpush('ticks', json.dumps(tick))
        time.sleep(0.001)  # Simulate 1000 ticks per second
