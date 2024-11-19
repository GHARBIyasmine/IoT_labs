import random
import time
import paho.mqtt.client as mqtt

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


# MQTT Configuration
broker = "192.168.64.131"  # Use your MQTT broker address
port = 1883
topic = "simulated/data"  # Topic for publishing data

# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker, port, 60)

# Create a simulator instance
sim = Simulator(seed=12345, mean=20, standard_deviation=5)

# Set a loop to publish data periodically
while True:
    # Generate next data point
    next_value = sim.calculate_next_value()

    # Publish the value to MQTT
    client.publish(topic, str(next_value))

    # Print the value to the console for monitoring
    print(f"Published: {next_value}")

    # Wait for some time before generating the next value (e.g., 1 second)
    time.sleep(3)
