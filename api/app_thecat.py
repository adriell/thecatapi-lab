from flask import Flask, send_file, jsonify, request, Response
from flask_restful import Api, Resource
from pymongo import MongoClient
from bson import json_util
import json
import bcrypt
import requests
import docker
import logging
from bson.json_util import dumps

 
logger = logging.getLogger(__name__)
app = Flask(__name__)
api = Api(app)

url = "https://api.thecatapi.com/v1/breeds"
headers = {'x-api-key': '41c95355-4fcc-499d-a0c7-a56c6b6ceefd'}
client = MongoClient("mongodb://db:27017")


db = client.thecatsDB
breeds = db["breeds"]

class GetAllBreeds(Resource):
    def get(self):

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

class GetBreeds(Resource):
    def get(self):
        breeds_cat = list(db.breeds.find())
        return json.dumps(breeds_cat, default=json_util.default)

class GetOrigin(Resource):
    def get(self):
        breeds_cat = list(db.breeds.find({},{"Origin": 1}))
        return json.dumps(breeds_cat, default=json_util.default)      

class GetBreedsOrigin(Resource):
    def post(self):
        data = request.get_json()
        breed = data["Origin"]
        result = list(db.breeds.find({"Origin": breed }))
        return json.dumps(result, default=json_util.default)

class GetBreed(Resource):
    def post(self):
        data = request.get_json()
        breed = data["Name"]
        result = list(db.breeds.find({"Name": breed}))
        return json.dumps(result, default=json_util.default)

class GetTemperament(Resource):
    def post(self):
        data = request.get_json()
        breed = data["Temperament"]
        result = list(db.breeds.find({"Temperament": { "$regex": breed }}))
        return json.dumps(result, default=json_util.default)

api.add_resource(GetAllBreeds, '/')
api.add_resource(GetBreeds, '/breeds') #Lista todas Raças
api.add_resource(GetBreedsOrigin, '/breedsorigin') #Lista as raças a partir do da origem
api.add_resource(GetOrigin, '/origin')
api.add_resource(GetBreed, '/breed') #Lista informações de uma raça
api.add_resource(GetTemperament, '/temperament') #Lista as raças a partir do temperamento

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
