#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

customers = [
    {
        'id' : 1,
        'name' : 'Paulo',
        'email' : 'paulo@user.com'
    },
    {
        'id' : 2,
        'name' : 'Cesar',
        'email' : 'cesar@user.com'
    }
]

@app.route('/Customers', methods = ['GET'])
def get_customers():
    return jsonify({'customers': customers})
    
@app.route('/Customers/<int:customer_id>', methods = ['GET'])
def get_customer_id(customer_id):
    customer = [customer for customer in customers if customer['id'] == customer_id]
    if len(customer) == 0:
        abort(404)
    return jsonify({'customer' : customer[0]})
    
@app.route('/Customers/<string:customer_name>', methods = ['GET'])
def get_customer_name(customer_name):
    customer = [customer for customer in customers if customer['name'] == customer_name]
    if len(customer) == 0:
        abort(404)
    return jsonify({'customer' : customer[0]})
    
@app.route('/Customers', methods = ['POST'])
def register_customer():
    if not request.json or not 'name' in request.json:
        abort(400)
    customer = {
        'id' : customers[-1]['id'] + 1,
        'name' : request.json['name'],
        'email' : request.json['email']
    }
    customers.append(customer)
    return jsonify({'customer' : customer}), 201
    
@app.route('/Customers/<int:customer_id>', methods = ['PUT'])
def update_customer(customer_id):
    customer = [customer for customer in customers if customer['id'] == customer_id]
    if len(customer) == 0:
        abort(404)
    if not request.json:
        abort(400)
    customer[0]['name'] = request.json.get('name', customer[0]['name'])
    customer[0]['email'] = request.json.get('email', customer[0]['email'])
    return jsonify({'customer' : customer})
    
@app.route('/Customers/<int:customer_id>', methods = ['DELETE'])
def delete_customer(customer_id):
    customer = [customer for customer in customers if customer['id'] == customer_id]
    if len(customer) == 0:
        abort(404)
    customers.remove(customer[0])
    return jsonify({'result' : True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found!'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)