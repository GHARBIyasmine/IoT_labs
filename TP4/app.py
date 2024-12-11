from flask import Flask, Response, render_template
import random
import time
import matplotlib.pyplot as plt
from io import BytesIO
import threading

app = Flask(__name__)

# Simuler les données
NUM_SENSORS = 5
data_buffers = {f"sensor_{i}": [] for i in range(NUM_SENSORS)}

def simulate_sensor_data():
    """Simulation des données en arrière-plan"""
    while True:
        for sensor_id in data_buffers.keys():
            value = random.randint(0, 100)
            if len(data_buffers[sensor_id]) >= 100:
                data_buffers[sensor_id].pop(0)
            data_buffers[sensor_id].append(value)
        time.sleep(0.5)

# Démarrer la simulation dans un thread
threading.Thread(target=simulate_sensor_data, daemon=True).start()


# Fonction pour créer un graphique dynamique
def create_plot():
    """Génération dynamique du graphique avec Matplotlib"""
    plt.figure(figsize=(10, 6))

    for sensor_id, values in data_buffers.items():
        plt.plot(values, label=sensor_id)

    plt.xlabel('Temps')
    plt.ylabel('Valeurs')
    plt.title('Simulation IoT en Temps Réel')
    plt.legend()
    plt.grid()
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


# Route principale pour l'affichage dynamique
@app.route('/')
def index():
    """Page principale avec AJAX pour l'affichage dynamique"""
    return render_template('index.html')


# Route pour l'image du graphique
@app.route('/plot')
def plot():
    buf = create_plot()
    return Response(buf, mimetype='image/png')


# Lancer le serveur
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
