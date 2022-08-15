import pprint
import random

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# 보통 "자동차" 와 같은 것들은 "데이터베이스" 에 저장되지만,
# 파이썬 리스트로 저장하기로 한다.
cars = []

class Car(Resource):
    '''
    Car 이라는 리소스를 다룰 것인데,
    get, post, delete, put 메서드들을 정의할 것이다.
    '''
    def get(self, name):
        car = next(filter(lambda x: x['name'] == name, cars), None)
        return {'car' : car}, 200 if car else 404

    def post(self, name):

        # 만약, 이미 존재하는 자동차의 이름으로 새 자동차를 생성해 달라는 요청이 들어오면,
        # error 메시지와 함께 400 상태 코드를 리턴
        if next(filter(lambda x: x['name'] == name, cars), None):
            return {'error' : f'{name} item already exists.'}, 400
        data = request.get_json()
        new_car = {'name' : name, 'price' : data['price']}
        cars.append(new_car)
        return new_car, 201

    def delete(self, name):
        pass

    def put(self, name):
        pass

class CarList(Resource):
    def get(self):
        return {'cars' : cars}

api.add_resource(Car, '/car/<string:name>')
api.add_resource(CarList, '/cars')

if __name__ == "__main__":
    app.run(debug=True)