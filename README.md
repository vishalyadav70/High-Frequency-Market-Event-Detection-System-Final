# High-Frequency Financial Tick Simulator

## Overview

This project implements a high-frequency financial tick simulation system that generates random price ticks for various financial instruments, detects significant price movements (spikes), logs these movements, and visualizes the data in real-time. 

### Objectives
1. **Random Tick Generator**: Continuously generates random price ticks for predefined financial instruments.
2. **Spike Detection**: Detects significant price movements (spikes) where the price change exceeds 10% from the last recorded price.
3. **Logging**: Logs detected price spikes to a CSV file with details including the instrument, old price, new price, and timestamp.
4. **Visualization** (Bonus): Provides a real-time visualization of price movements using Dash and Plotly.
5. **Messaging Queues for Scalability** (Bonus): Utilizes Redis to handle high-frequency data flow and supports scalability.

## Project Structure

The project is organized into several files:

- `config.py`: Configuration settings for financial instruments, initial prices, Redis setup, and log file path.
- `tick_generator.py`: Generates random price ticks and enqueues them into Redis.
- `spike_detector.py`: Detects price spikes, logs them, and maintains price history.
- `visualization.py`: Provides real-time visualization of price data using Dash and Plotly.
- `main.py`: Starts the tick generator and the Dash application.

## Setup Instructions

1. **Install Dependencies**

   Ensure you have Python 3.x installed. Then, install the required packages using pip:

   ```bash
   pip install redis dash plotly pytz
2. **Install and Start Redis Server**

## Running the System

1. **To start the tick generation and real-time visualization, run the main.py script:**

    
     ```bash
    python main.py

2. **This command will**

    1. Start a separate thread to continuously generate and enqueue price ticks.
    2. Run a Dash application that provides real-time visualization of the price movements.
    