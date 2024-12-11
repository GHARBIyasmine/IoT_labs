from flask import Flask, Response, render_template
import random
import time
import matplotlib.pyplot as plt
from io import BytesIO
import threading

app = Flask(__name__)

# Simulate number of sensors (for simplicity, 1 sensor monitoring power usage)
NUM_SENSORS = 1
data_buffers = {f"sensor_{i}": [] for i in range(NUM_SENSORS)}

# Define the threshold to simulate a "spike"
POWER_SPIKE_THRESHOLD = 70


def simulate_sensor_data():
    """Simulate real-time power usage data in the background."""
    while True:
        for sensor_id in data_buffers.keys():
            # Simulate power usage value between 0 and 100
            value = random.randint(0, 100)
            
            # Ensure we only keep the most recent 100 data points
            if len(data_buffers[sensor_id]) >= 100:
                data_buffers[sensor_id].pop(0)

            # Append new simulated power usage value
            data_buffers[sensor_id].append(value)
        
        time.sleep(0.5)  # Simulate data update every 0.5 seconds


# Start data simulation in a background thread
threading.Thread(target=simulate_sensor_data, daemon=True).start()


def create_plot():
    """Generate dynamic real-time power usage plot with spike detection."""
    plt.figure(figsize=(12, 6))

    for sensor_id, values in data_buffers.items():
        # Detect spikes for visualization
        x_values = range(len(values))
        spikes = [v if v > POWER_SPIKE_THRESHOLD else None for v in values]

        # Plot the general power usage line
        plt.plot(x_values, values, label=f"{sensor_id} Power Usage")
        
        # Highlight spikes
        plt.scatter(
            [i for i, v in enumerate(spikes) if v is not None],
            [v for v in spikes if v is not None],
            color="red",
            label="Spike",
            s=20,
        )

    # Set axis labels, title, and legend
    plt.xlabel('Time')
    plt.ylabel('Power Usage (in Watts)')
    plt.title('Real-Time Power Usage with Spike Detection')
    plt.legend()
    plt.grid()

    # Save plot to buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


# Route for main page
@app.route('/')
def index():
    """Render the main HTML template with dynamic updates via AJAX."""
    return render_template('index.html')


# Route to dynamically fetch the generated plot
@app.route('/plot')
def plot():
    buf = create_plot()
    return Response(buf, mimetype='image/png')


# Launch the server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
