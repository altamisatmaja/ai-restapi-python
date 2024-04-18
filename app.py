from flask import Flask, jsonify
import numpy as np
from sklearn.neighbors import NearestNeighbors
from haversine import haversine
import requests
from dotenv import load_dotenv
import os

from locale import str

from builtins import Exception, float

app = Flask(__name__)

load_dotenv()

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

@app.route('/product', methods=['GET'])
def product_nearest():
    response = requests.get('http://127.0.0.1:8000/api/auth/product/nearest')
    if response.status_code == 200:
        data = response.json()

        lokasi = [(float(item['partner'][0]['latitude']), float(item['partner'][0]['longitude'])) for item in data['data']]

        lokasi_saat_ini = (-6.2088, 106.8456)

        jarak = [haversine(lokasi_saat_ini, loc) for loc in lokasi]

        jarak_terdekat = np.argsort(jarak)[:5]

        produk_terdekat = [data['data'][i] for i in jarak_terdekat]
        return jsonify(produk_terdekat)
    else:
        return jsonify({'status': 'error', 'message': 'Gagal mendapat data dari API.'}), 500

@app.route('/nearest', methods=['GET'])
def nearest():
    response = requests.get('http://127.0.0.1:8000/api/auth/product/nearest')

    if response.status_code == 200:
        data = response.json()
        
        if data.get('status') and data.get('data'):
            product_data = []
            
            for product in data['data']:
                id_product = product.get('id')
                gambar_hewan = product.get('gambar_hewan')
                id_typelivestocks = product.get('id_typelivestocks')
                terjual = product.get('terjual')
                id_jenis_gender_hewan = product.get('id_jenis_gender_hewan')
                harga_product = product.get('harga_product')
                latitude = product.get('partner')[0].get('latitude')
                longitude = product.get('partner')[0].get('longitude')
                provinsi_partner = product.get('partner')[0].get('provinsi_partner')
                product_data.append({
                    'id_product': id_product,
                    'gambar_hewan': gambar_hewan,
                    'id_typelivestocks': id_typelivestocks,
                    'terjual': terjual,
                    'id_jenis_gender_hewan': id_jenis_gender_hewan,
                    'harga_product': harga_product,
                    'latitude': latitude,
                    'longitude': longitude,
                    'provinsi_partner': provinsi_partner
                })
            
            return jsonify({'status': 'success', 'data': product_data})
        else:
            return jsonify({'status': 'error', 'message': 'Tidak ada data.'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Gagal mengambil data.', 'status_code': response.status_code}), 500


if __name__ == '__main__':
    app.run(debug=True)
