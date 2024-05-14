from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
from sklearn.neighbors import NearestNeighbors
from haversine import haversine
import requests
from dotenv import load_dotenv
import os

from locale import str

from builtins import Exception, ValueError, float, map, tuple

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.route('/product/<string:latitude_user>/<string:longitude_user>/', methods=['GET'])
@cross_origin()
def product_nearest(latitude_user, longitude_user):
    try:
        latitude = float(latitude_user)
        longitude = float(longitude_user)
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid latitude or longitude parameter.'}), 400

    response = requests.get('http://127.0.0.1:8000/api/product/nearest')
    if response.status_code == 200:
        data = response.json()

        lokasi = [(float(item['partner'][0]['latitude']), float(item['partner'][0]['longitude'])) for item in data['data']]

        lokasi_saat_ini = (latitude, longitude)

        jarak = [haversine(lokasi_saat_ini, loc) for loc in lokasi]

        jarak_terdekat = np.argsort(jarak)[:10]

        produk_terdekat = [data['data'][i] for i in jarak_terdekat]
        response_target = jsonify(produk_terdekat)
        # response_target.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:8000/')
        
        return response_target
    else:
        return jsonify({'status': 'error', 'message': 'Gagal mendapat data dari API.'}), 500

@app.route('/nearest', methods=['GET'])
@cross_origin()
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
            
            return jsonify({'status': 'success', 'product': product_data})
        else:
            return jsonify({'status': 'error', 'message': 'Tidak ada data.'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Gagal mengambil data.', 'status_code': response.status_code}), 500


if __name__ == '__main__':
    app.run(debug=True)
