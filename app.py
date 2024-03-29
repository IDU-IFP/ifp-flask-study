from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

animals = []

class Animal(Resource):
  def get(self, name):
    for animal in animals:
      if animal['name'] == name:
        return animal
    return {'animal' : None}, 404
  
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
     return {'message' : f'animal <{name}> deleted successfully!'}, 200
   else:
     return {'message' : f'animal <{name}> not found.'}, 400
  
  def put(self, name):
    data = request.get_json()
    animal = next(filter(lambda x: x['name'] == name, animals), None)
    if animal is None:
      animal = {'name' : name, 'age' : data['age']}
      animals.append(animal)
    else:
      animal.update(data)
    return animal
  
class AnimalList(Resource):
  def get(self):
    return {'animals' : animals}
  
api.add_resource(Animal, '/animal/<string:name>')
api.add_resource(AnimalList, '/animals')

if __name__ == "__main__":
  app.run(debug=True)