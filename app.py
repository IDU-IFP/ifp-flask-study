from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

animals = [{'name': 'cat', 'age': 10}, ]


class Animal(Resource):

    def get(self, name):
        for animal in animals:
            if animal['name'] == name:
                return animal, 200
        else:
            return {'message': f'animal<{name}> is not found'}, 404

    def post(self, name):
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        if animal is None:
            data = request.get_json()
            animal = {'name': name, 'age': data['age']}
            animals.append(animal)
            return animal, 201
        else:
            return {'message': f'animal <{name}> is already in the list'}, 400

    def put(self, name):
        data = request.get_json()
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        if animal is None:
            animal = {'name': name, 'age': data['age']}
            animals.append(animal)
            return animal, 201
        else:
            animal.update(data)
            return animal, 200

    def delete(self, name):
        # animal = animal = next(filter(lambda x: x['name'] == name, animals), None)
        # animals = list(filter(lambda x: x['name'] != 'name', animals))
        # if animal is True:
        #     return {'message' : f'animal <{name}> deleted successfully!'}, 200
        # else:
        #     return {'message' : f'animal <{name}> not found.'}, 404
        animal = next(filter(lambda x: x['name'] == name, animals), None)
        if animal is None:
            return {'message': f'animal <{name}> is not found.'}, 404
        else:
            del(animals['name' == name])
            return {'message': f'animal <{name}> deleted successfully!'}, 200


class AnimalList(Resource):
    def get(self):
        return {'animals': animals}


api.add_resource(Animal, '/animal/<string:name>')
api.add_resource(AnimalList, '/animals')

if __name__ == "__main__":
    app.run(debug=True)
