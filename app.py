from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

shop_list = [
    {
        'name' : 'Smith flower store',
        'items' : [
            {
                'name' : '물망초',
                'price' : '1200',
            }
        ]
    },
]


'''
서버의 입장에서,
POST -  클라이언트가 보낸 데이터를 받는 데에 사용한다.
GET  -  데이터를 다시 돌려주는 데에만 사용한다.

ex) /shop                        -> 새로운 shop을 생성하거나, shop 목록을 보여줌
    /shop/smith-flower-shop      -> shop들 중, smith-flower-shop이라는 이름을 가진 것을 보여줌
    /shop/smith-flower-shop/item -> smith-flower-shop에 새로운 item을 생성하거나, smith-flower-shop에 있는 item들 목록을 보여줌
'''

# 아래에서 다룰 리소스들 : shop, item

# POST /shop -> name 이라는 데이터를 받아서, 새로운 shop을 생성함
@app.route('/shop', methods=['POST'])
def create_shop():
    request_data = request.get_json()
    new_shop = {
        'name' : request_data['name'],
        'items' : []
    }
    shop_list.append(new_shop)
    return jsonify(new_shop)

# GET  /shop/<string:name> -> name 에 맞는 shop 을 보여줌
@app.route('/shop/<string:shop_name>', methods=['GET'])
def get_shop_detail(shop_name):
    for shop in shop_list:
        if shop['name'] == shop_name:
            return jsonify(shop)
    return jsonify({'message' : 'shop not found'})

# GET  /shop -> shop의 목록들을 보여줌
@app.route('/shop', methods=['GET'])
def get_shop_list():
    return jsonify({'shop_list':shop_list})

# POST /shop/<string:shop_name>/item -> item_name, price 를 받아서, name에 맞는 shop에 새로운 item을 추가
@app.route('/shop/<string:shop_name>/item', methods=['POST'])
def create_item_in_shop(shop_name):
    request_data = request.get_json()
    for shop in shop_list:
        if shop['name'] == shop_name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            shop['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message' : 'shop not found'})

# GET  /shop/<string:name>/item -> shop에 들어있는 item들의 목록을 반환
@app.route('/shop/<string:shop_name>/item', methods=['GET'])
def get_item_list_in_shop(shop_name):
    for shop in shop_list:
        if shop['name'] == shop_name:
            return jsonify({'items' : shop['items']})
    return jsonify({'message': 'shop not found'})

if __name__ == '__main__':
    app.run()
