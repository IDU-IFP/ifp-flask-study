import pprint
import random

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

animals = []

class animal(Resource):
    def get(self, name):
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        return {'animal' : animal}, 200 if animal else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, animals), None):
            return {'error' : f'{name} item already exists.'}, 400
        data = request.get_json()
        new_animal = {'name' : name, 'age' : data['age']}
        animals.append(new_animal)
        return new_animal, 201

    def delete(self, name):
        global animals
        animal = animal = next(filter(lambda x: x['name'] == name, animals), None)
        animals = list(filter(lambda x : x['name'] != name, animals))
        if animal:
            return {'message': f'animal <{name}> deleted successfully!'}, 200
        else:
            return {'message': f'animal <{name}> not found.'}, 404

    def put(self, name):
        data = request.get_json()
        animal=next(filter(lambda x: x['name']==name, animals), None)
        if animal is None:
            animal={'name':name, 'age': data['age']}
            animals.append(animal)
        else:
            animal.update(data)
        return animal

class animalList(Resource):
    def get(self):
        return {'animals' : animals}

api.add_resource(animal, '/animal/<string:name>')
api.add_resource(animalList, '/animals')

if __name__ == "__main__":
    app.run(debug=True)