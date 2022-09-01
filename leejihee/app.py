import pprint
import random

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

cars = []

class Car(Resource):
    def get(self, name):
        car = next(filter(lambda x: x['name'] == name, cars), None)
        return {'car' : car}, 200 if car else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, cars), None):
            return {'error' : f'{name} item already exists.'}, 400
        data = request.get_json()
        new_car = {'name' : name, 'price' : data['price']}
        cars.append(new_car)
        return new_car, 201

    def delete(self, name):
        global cars
        car = car = next(filter(lambda x: x['name'] == name, cars), None)
        cars = list(filter(lambda x : x['name'] != name, cars))
        if car:
            return {'message': f'car <{name}> deleted successfully!'}, 200
        else:
            return {'message': f'car <{name}> not found.'}, 404

    def put(self, name):
        data = request.get_json()
        car=next(filter(lambda x: x['name']==name, cars), None)
        if car is None:
            car={'name':name, 'price': data['price']}
            cars.append(car)
        else:
            car.update(data)
        return car

class CarList(Resource):
    def get(self):
        return {'cars' : cars}

api.add_resource(Car, '/car/<string:name>')
api.add_resource(CarList, '/cars')

if __name__ == "__main__":
    app.run(debug=True)