from flask import Flask, jsonify
import numpy as np
from sklearn.neighbors import NearestNeighbors
from haversine import haversine

app = Flask(__name__)

data_alamat = [
    {"kota": "Ngawi", "latitude": -6.2088, "longitude": 106.8456},
    {"kota": "Jember", "latitude": -7.2575, "longitude": 112.7521},
    {"kota": "Jokowi", "latitude": -6.9175, "longitude": 107.6191},
    {"kota": "Anis", "latitude": -6.1751, "longitude": 106.865},
    {"kota": "Ganjar", "latitude": -7.2761, "longitude": 112.7916},
    {"kota": "Ganjar", "latitude": -7.2761, "longitude": 112.7916},
    {"kota": "Ganjar", "latitude": -7.2761, "longitude": 112.7916},
    {"kota": "Ganjar", "latitude": -7.2761, "longitude": 112.7916},
]

data = np.array([[kota['latitude'], kota['longitude']] for kota in data_alamat])

lokasi_saat_ini = np.array([-6.2088, 106.8456])

distances = [haversine((lokasi_saat_ini[0], lokasi_saat_ini[1]), (lat, lon)) for lat, lon in data]

indeks = np.argsort(distances)[:7]

jarak_terdekat = [data_alamat[i] for i in indeks]

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({'data' : jarak_terdekat})

if __name__ == '__main__':
    app.run(debug=True)
