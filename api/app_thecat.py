from flask import Flask, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from logging.config import dictConfig
import bcrypt
import requests
from flask_prometheus_metrics import register_metrics


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)

url = "https://api.thecatapi.com/v1/breeds"
headers = {'x-api-key': '41c95355-4fcc-499d-a0c7-a56c6b6ceefd'}
client = MongoClient("mongodb://db:27017")


db = client.thecatsDB
breeds = db["breeds"]

@app.route('/breeds', methods=["GET"])
def cats():
    response = requests.get(url, headers=headers)
    r = response.json()
    for i in range(len(r)):
        breeds.insert_one({ 
            "Name":  r[i]['name'],
            "Origin": r[i]['origin'],
            "Temperament": r[i]['temperament'],
            "Description": r[i]['description']
        })
    
    return response.text
@app.route('/breeds/images', methods=["GET"])
def images():
    response = requests.get("https://api.thecatapi.com/v1/images/search" )


#Register Metrics
register_metrics(app)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
