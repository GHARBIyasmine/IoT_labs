import paho.mqtt.client as mqtt
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Global variables
plot_data_list = []  # Data for plotting
plot_time_stamps = []  # Timestamps for plotting
process_data_list = []  # Data for processing (to calculate moving average)
period = 4  # Sampling period in seconds
window_size = 3  # Window size for moving average

# Broker configurations
input_broker_address = "192.168.64.131"  # Input broker
input_topic = "top/simulated"
output_broker_address = "192.168.64.1"  # Output broker
output_topic = "top/filtered"

# Lock for thread-safe data access
data_lock = threading.Lock()

# Callback function when a message is received
def on_message(client, userdata, message):
    try:
        value = float(message.payload.decode("utf-8"))
        timestamp = time.time()
        with data_lock:
            plot_data_list.append(value)
            plot_time_stamps.append(timestamp)
            process_data_list.append(value)
        print(f"Received data: {value}")
    except ValueError:
        print(f"Invalid data received: {message.payload.decode('utf-8')}")

# Function to calculate the moving average
def moving_average(data, window_size):
    """Calculates moving average over a sliding window."""
    moving_averages = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        window_average = round(sum(window) / window_size, 2)
        moving_averages.append(window_average)
    return moving_averages

# Function to process and publish filtered data periodically
def process_and_publish():
    output_client = mqtt.Client("Filtered_Publisher")
    output_client.connect(output_broker_address)
    while True:
        time.sleep(period)  # Wait for the sampling period
        with data_lock:
            if len(process_data_list) >= window_size:
                # Calculate moving average over the last `window_size` elements
                moving_avg = moving_average(process_data_list, window_size)
                # Publish the latest moving average
                latest_avg = moving_avg[-1]  # Get the last moving average value
                output_client.publish(output_topic, f"{latest_avg:.2f}")
                print(f"Published moving average: {latest_avg:.2f}")
            else:
                print("Not enough data to calculate moving average.")
            # Clear the data list after processing (optional depending on use case)
            process_data_list.clear()

# Function to update the real-time plot
def update_plot(frame):
    with data_lock:
        if plot_time_stamps and plot_data_list:
            plt.cla()  # Clear the current plot
            plt.plot(plot_time_stamps, plot_data_list, label="Received Data", color="blue")
            plt.title("Real-Time Data Plot")
            plt.xlabel("Time")
            plt.ylabel("Data Value")
            plt.legend()
            plt.tight_layout()

# Main MQTT client setup
def start_mqtt_client():
    input_client = mqtt.Client("Receiver")
    input_client.on_message = on_message
    input_client.connect(input_broker_address)
    input_client.subscribe(input_topic)
    print("Starting data reception...")
    input_client.loop_forever()

# Main execution
if __name__ == "__main__":
    # Start the periodic processing in a separate thread
    processing_thread = threading.Thread(target=process_and_publish)
    processing_thread.daemon = True
    processing_thread.start()

    # Start the MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    # Set up the real-time plot
    plt.figure()
    ani = FuncAnimation(plt.gcf(), update_plot, interval=1000)

    # Run the plot in the main thread
    plt.show()
