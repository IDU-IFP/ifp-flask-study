import random
from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

animals=[
    {
        'name' : 'turtle',
        'age' : 200
    },
    {
        'name' : 'dolphin',
        'age' : 2
    },
    {
        'name' : 'shark',
        'age' : 5
    },
    {
        'name' : 'beluga',
        'age' : 15
    },
]
class Animal(Resource):
    def get(self, name):
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        return {'animal' : animal}, 200 if animal else 404
    
    def post(self, name):
        #이미 존재하는 동물의 이름으로 POST 요청이 들어오면 에러 메세지와 함께 400 상태코드 리턴
        if next(filter(lambda x : x['name'] == name, animals), None):
            return {'error' : f'{name} item already exists.'}, 400
        data = request.get_json()
        new_animal = {'name' : name, 'age' : data['age']}
        animals.append(new_animal)
        return new_animal, 201
    
    def delete(self, name):
        global animals
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        animals = list(filter(lambda x : x['name'] != name, animals))
        if animal:
            return {'message' : f'car <{name}> deleted successfully!'}, 200
        else:
            return {'message' : f'car <{name}> not found.'}, 404
    
    def put(self, name):
        data = request.get_json()
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        if animal is None:
            animal = {'name': name, 'age' : data['age']}
            animals.append(animal)
        else:
            animal.update(data)
        return animal

class AnimalList(Resource):
    def get(self):
        return {'animals': animals}

  
api.add_resource(Animal, '/animal/<string:name>')
api.add_resource(AnimalList, '/animals')

if __name__ == "__main__":
    app.run(debug=True)