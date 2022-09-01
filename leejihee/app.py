from flask import Flask
from flask_restful import Resource, Api
import random

app=Flask(__name__)
api=Api(app)

cars=[]

class Car(Resource):
    def get(self, name):
        for car in cars:
            if car['name'] == name:
                return car
            
    def post(self, name):
        car={'name': name, 'price':random.randrange(1000000, 1000000000)}
        cars.append(car)
        return car
    
    def delete(self, name):
        pass
    def put(self, name):
        pass
    
api.add_resource(Car, '/car/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)