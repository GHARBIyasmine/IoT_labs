import time
import random
import math
import threading
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# MQTT broker addresses and topics
PUBLISH_BROKER_ADDRESS = "192.168.64.131"  # Broker to send generated data
RECEIVE_BROKER_ADDRESS = "192.168.64.1"    # Broker to receive processed data
PUBLISH_TOPIC = "top/simulated"
RECEIVE_TOPIC = "top/filtered"

# Global data lists
generated_data = []
generated_timestamps = []
received_data = []
received_timestamps = []


# Simulator class to generate data
class Simulator:
    _factors = [-1, 1]

    def __init__(self, seed, mean, standard_deviation):
        self._random = random.Random(seed)
        self._mean = mean
        self._standard_deviation = abs(standard_deviation)
        self._step_size_factor = self._standard_deviation / 10
        self._value = self._mean - self._random.random()

    def calculate_next_value(self):
        value_change = self._random.random() * self._step_size_factor
        factor = self._factors[self.decide_factor()]
        self._value += value_change * factor
        return self._value

    def decide_factor(self):
        if self._value > self._mean:
            distance = self._value - self._mean
            continue_direction, change_direction = 1, 0
        else:
            distance = self._mean - self._value
            continue_direction, change_direction = 0, 1

        chance = (self._standard_deviation / 2) - (distance / 50)
        random_value = self._random.random() * self._standard_deviation

        return continue_direction if random_value < chance else change_direction


# Function to compute the next time interval (Poisson distributed)
def next_time_interval(l):
    n = random.random()
    inter_event_time = -math.log(1.0 - n) / l
    return inter_event_time


# MQTT callback for receiving data
def on_message(client, userdata, message):
    global received_data, received_timestamps
    try:
        value = float(message.payload.decode("utf-8"))
        received_data.append(value)
        received_timestamps.append(time.time())
        print(f"Received data: {value}")
    except ValueError:
        print(f"Invalid data received: {message.payload.decode('utf-8')}")


# Real-time plotting functions
def update_plot(frame):
    global generated_data, generated_timestamps, received_data, received_timestamps
    plt.cla()  # Clear the axis to avoid overlapping
    if generated_timestamps and received_timestamps:
        # Plot both generated and received data on the same plot
        plt.plot(generated_timestamps, generated_data, label="Generated Data", color="blue")
        plt.plot(received_timestamps, received_data, label="Received Data", color="orange")
        plt.title("Real-Time Data Comparison")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()


# Function to continuously publish generated data
def continuous_pub_poisson(client, simulator, l):
    global generated_data, generated_timestamps
    while True:
        interval = next_time_interval(l)
        time.sleep(interval)  # Wait for the next interval
        value = simulator.calculate_next_value()
        message = f"{value:.2f}"
        client.publish(PUBLISH_TOPIC, message)
        generated_data.append(value)
        generated_timestamps.append(time.time())
        print(f"Published: {message} | Interval: {interval:.2f}s")


# Main function
def main():
    global generated_data, received_data

    # MQTT client setup for publishing
    publish_client = mqtt.Client()  # Explicitly using protocol version 3.1.1
    publish_client.connect(PUBLISH_BROKER_ADDRESS)

    # MQTT client setup for receiving
    receive_client = mqtt.Client()
    receive_client.on_message = on_message
    receive_client.connect(RECEIVE_BROKER_ADDRESS)
    receive_client.subscribe(RECEIVE_TOPIC)
    receive_client.loop_start()  # Start the loop for receiving messages

    # Initialize the simulator
    simulator = Simulator(seed=12345, mean=20, standard_deviation=5)
    lambda_value = 10  # Events per second on average

    # Start the publishing in a separate thread
    publish_thread = threading.Thread(target=continuous_pub_poisson, args=(publish_client, simulator, lambda_value))
    publish_thread.daemon = True
    publish_thread.start()

    # Set up real-time plot
    plt.figure(figsize=(10, 6))
    ani = FuncAnimation(plt.gcf(), update_plot, interval=1000, cache_frame_data=False)

    print("Starting real-time data visualization...")
    try:
        plt.tight_layout()
        plt.show()
    except KeyboardInterrupt:
        print("Exiting...")
        receive_client.loop_stop()


if __name__ == "__main__":
    main()

