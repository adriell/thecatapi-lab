# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource
from flask_restful_swagger import swagger
from pymongo import MongoClient
import bcrypt
import requests
 
app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1',
                   basePath='http://localhost:5000/',
                   resourcePath='/',
                   produces=["application/json","text/html"],
                   api_spec_url='/api/spec')

url = "https://api.thecatapi.com/v1/breeds"
headers = {'x-api-key': '41c95355-4fcc-499d-a0c7-a56c6b6ceefd'}
client = MongoClient("mongodb://db:27017")


db = client.thecatsdb
breeds = db["breeds"]

class GetAllBreeds(Resource):
    @swagger.operation(
      notes='Get all breeds',
      nickname='get')
    def get(self):
        response = requests.get(url, headers=headers)
        r = response.json()
        for i in range(len(r)):
            breeds.insert_one({ 
                "_id": i + 1,
                "Name":  r[i]['name'],
                "Origin": r[i]['origin'],
                "Temperament": r[i]['temperament'],
                "Description": r[i]['description']
            })

        return "It works!"

class GetBreeds(Resource):
    @swagger.operation(
      notes='Get all breeds in mongodb',
      nickname='get')
    def get(self):
        breeds_cat = list(db.breeds.find({},{"Name":1}))
        return breeds_cat

class GetOrigin(Resource):
    @swagger.operation(
      notes='Get all origin',
      nickname='get')
    def get(self):
        breeds_cat = list(db.breeds.find({},{"Origin": 1}))
        return breeds_cat

class GetBreedsOrigin(Resource):
    @swagger.operation(
      notes='Get all breeds by origin',
      nickname='post',
      parameters=[
          {
            "name": "Origin",
            "description": "Origin of the breeds",
            "required": True,
            "allowMultiple": False,
            "dataType": 'string',
            "paramType": "body"
          }
      ])
    def post(self):
        data = request.get_json()
        origin = data["Origin"]
        result = [i for i in db.breeds.find({"Origin": origin },{"Name": 1} )]
        return result

class GetBreed(Resource):
    @swagger.operation(
      notes='Get all breeds by name',
      nickname='post',
      parameters=[
          {
            "name": "Name",
            "description": "Name of the breeds",
            "required": True,
            "allowMultiple": False,
            "dataType": 'string',
            "paramType": "body"
          }
      ])
    def post(self):
        data = request.get_json()
        breed = data["Name"]
        result = db.breeds.find_one({"Name": breed})
        
        return result

class GetTemperament(Resource):
    @swagger.operation(
      notes='Get all breeds by temperament',
      nickname='post',
      parameters=[
          {
            "name": "Temperament",
            "description": "Temperament of the breeds",
            "required": True,
            "allowMultiple": False,
            "dataType": 'string',
            "paramType": "body"
          }
      ])
    def post(self):
        data = request.get_json()
        temperament = data["Temperament"]
        result = [i for i in db.breeds.find({"Temperament": { "$regex": temperament }}, {"Name":1})]
        return result

api.add_resource(GetAllBreeds, '/savebreeds')
api.add_resource(GetBreeds, '/breeds') #Lista todas Raças
api.add_resource(GetBreedsOrigin, '/breedsorigin') #Lista as raças a partir do da origem
api.add_resource(GetOrigin, '/origin')
api.add_resource(GetBreed, '/breed') #Lista informações de uma raça
api.add_resource(GetTemperament, '/temperament') #Lista as raças a partir do temperamento

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
