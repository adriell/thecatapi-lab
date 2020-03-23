from flask import Flask, send_file, jsonify, request, Response
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import docker
import logging

 
logger = logging.getLogger(__name__)
app = Flask(__name__)

url = "https://api.thecatapi.com/v1/breeds"
headers = {'x-api-key': '41c95355-4fcc-499d-a0c7-a56c6b6ceefd'}
client = MongoClient("mongodb://db:27017")


db = client.thecatsDB
breeds = db["breeds"]

def verifyBreed(breed):
    if breeds.find({"Name": name}).count() == 0:
        return False
    else:
        return True

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
    
    return "It works!"

@app.route('/breeds/images', methods=["GET"])
def images():
    response = requests.get("https://api.thecatapi.com/v1/images/search" )
    return "It works"

@app.route('/breedscat', methods=["GET"])
def breeds():
    breeds_cat = breeds.find()
    print (breeds_cat)
    result = {
        "status": 200,
        "result": breeds_cat
    }
    return jsonify(result)
@app.route('/breedinfo')
def post():
    data = request.get_json()
    breed = data["_id"]
    
    r = breeds.find({"_id": breed})
    restJson = {
        "status": 200,
        "obj": r
    }
    return jsonify(restJson)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
