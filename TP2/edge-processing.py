import paho.mqtt.client as mqtt
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Global variables
plot_data_list = []  # Data for plotting
plot_time_stamps = []  # Timestamps for plotting
process_data_list = []  # Data for processing (to calculate mean)
period = 5  # Sampling period in seconds

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


# Function to process and publish filtered data periodically
def process_and_publish():
    output_client = mqtt.Client("Filtered_Publisher")
    output_client.connect(output_broker_address)
    while True:
        time.sleep(period)  # Wait for the sampling period
        with data_lock:
            if process_data_list:
                mean_value = sum(process_data_list) / len(process_data_list)
                output_client.publish(output_topic, f"{mean_value:.2f}")
                print(f"Published mean: {mean_value:.2f}")
                process_data_list.clear()
            else:
                print("No data to process during this period.")


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
