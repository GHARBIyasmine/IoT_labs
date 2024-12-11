from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)

# Simuler des capteurs IoT
NUM_SENSORS = 5  # Nombre de capteurs simulés
data_buffers = {f"sensor_{i}": [] for i in range(NUM_SENSORS)}  # Simuler un buffer de données par capteur

# Fonction pour simuler la collecte de données
def simulate_sensor_data():
    while True:
        for sensor_id in data_buffers.keys():
            # Générer une valeur aléatoire pour chaque capteur
            value = random.randint(0, 100)
            # Limiter la taille du buffer à 10 valeurs
            if len(data_buffers[sensor_id]) >= 10:
                data_buffers[sensor_id].pop(0)
            data_buffers[sensor_id].append(value)
        time.sleep(1)  # Simuler une collecte toutes les secondes

# Démarrer la simulation des capteurs dans un thread séparé
threading.Thread(target=simulate_sensor_data, daemon=True).start()

# Route pour exposer les données agrégées
@app.route('/data', methods=['GET'])
def get_aggregated_data():
    aggregated_data = {}
    for sensor_id, data in data_buffers.items():
        # Calculer la moyenne des dernières valeurs
        aggregated_data[sensor_id] = sum(data) / len(data) if data else 0
    return jsonify(aggregated_data)

# Lancer l'API Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
