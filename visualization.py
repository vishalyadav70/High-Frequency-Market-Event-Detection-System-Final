# visualization.py

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import redis
from collections import deque
from spike_detector import detect_spikes, price_history  # Import price_history
from config import INSTRUMENTS, REDIS_HOST, REDIS_PORT, REDIS_DB

# Initialize data storage
xdata = deque(maxlen=100)
ydata = {instrument: deque(maxlen=100) for instrument in INSTRUMENTS}

# Redis client setup
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Real-Time Financial Instrument Price Movements", style={'textAlign': 'center', 'color': '#003366'}),
    dcc.Graph(id='live-update-graph', style={'height': '80vh'}),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every second
        n_intervals=0
    )
], style={'padding': '20px', 'backgroundColor': '#f8f9fa'})

@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    """Update the graph with the latest data from Redis."""
    while redis_client.llen('ticks') > 0:
        _, tick_str = redis_client.brpop('ticks')
        try:
            tick = json.loads(tick_str)
            detect_spikes(tick)
            # Update ydata for visualization
            for instrument in INSTRUMENTS:
                ydata[instrument].append(price_history[instrument])
        except json.JSONDecodeError:
            print("Error decoding tick data from Redis.")

    fig = make_subplots(
        rows=len(INSTRUMENTS), 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.1,  # Increased spacing between plots for more padding
        subplot_titles=[f"Price Movement of {instrument}" for instrument in INSTRUMENTS]
    )
    
    y_ranges = {}
    padding_factor = 0.1  # 10% padding for better visibility
    
    for i, instrument in enumerate(INSTRUMENTS):
        trace = go.Scatter(
            x=list(range(len(ydata[instrument]))),
            y=list(ydata[instrument]),
            mode='lines+markers',  # Lines with markers for better visibility
            name=instrument,
            line=dict(width=2, color=f'rgba({i * 50 + 100}, {i * 80 + 50}, {i * 30 + 100}, 1)'),  # Color coding
            marker=dict(size=8)  # Larger marker size
        )
        fig.add_trace(trace, row=i+1, col=1)
        
        # Calculate dynamic y-axis range for each subplot with padding
        if len(ydata[instrument]) > 1:
            y_min = min(ydata[instrument])
            y_max = max(ydata[instrument])
            y_range = y_max - y_min
            y_ranges[instrument] = (
                y_min - y_range * padding_factor,
                y_max + y_range * padding_factor
            )
        else:
            y_ranges[instrument] = (
                price_history[instrument] * 0.9,
                price_history[instrument] * 1.1
            )

    fig.update_layout(
        title='Real-Time Price Movements',
        title_x=0.5,  # Center title
        xaxis_title='Time (Ticks)',
        xaxis=dict(
            showline=True,
            showgrid=True,
            zeroline=False,
            showticklabels=True,
            title_standoff=10,
            title_text='Time (Ticks)'  # X-axis label
        ),
        showlegend=True,
        plot_bgcolor='#e5ecf6',  # Background color
        paper_bgcolor='#ffffff',  # Paper background color
        height=1200  # Increased height for better visibility
    )

    # Update y and x axis labels for each subplot and add borders
    for i, instrument in enumerate(INSTRUMENTS):
        fig.update_yaxes(
            title_text="Price",
            range=y_ranges[instrument],
            row=i+1, col=1,
            showline=True,  # Show border line
            linewidth=2,  # Width of the border
            linecolor='black'  # Color of the border
        )
        fig.update_xaxes(
            title_text="Time (Ticks)",
            row=i+1, col=1,
            showline=True,  # Show border line
            linewidth=2,  # Width of the border
            linecolor='black'  # Color of the border
        )

    return fig
