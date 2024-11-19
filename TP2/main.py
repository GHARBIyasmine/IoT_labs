import random
import matplotlib.pyplot as plt


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


# Generate data
data_set = []
sim = Simulator(seed=12345, mean=20, standard_deviation=5)

num_points = 5000

for i in range(num_points):
    data_set.append(sim.calculate_next_value())

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data_set, color="blue", linewidth=0.5)
plt.title("Simulated Data")
plt.xlabel("Iteration")
plt.ylabel("Value")
plt.show()
