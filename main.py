# main.py

import threading
from tick_generator import generate_and_enqueue_ticks
from visualization import app

def main():
    # Start the tick generator in a separate thread
    tick_thread = threading.Thread(target=generate_and_enqueue_ticks, daemon=True)
    tick_thread.start()
    
    # Start the Dash application
    app.run_server(debug=False)

if __name__ == "__main__":
    main()
