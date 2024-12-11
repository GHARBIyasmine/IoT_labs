from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# Data simulation
def generate_data():
    while True:
        vibration = random.uniform(0, 10)
        is_anomaly = vibration > 8
        yield {"timestamp": time.time(), "vibration": vibration, "is_anomaly": is_anomaly}
        time.sleep(0.5)

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/data')
def data():
    return jsonify(next(data_stream))

# Start data simulation generator
data_stream = generate_data()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
