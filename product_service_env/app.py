from flask import Flask, request, jsonify

app = Flask(__name__)

products = {}  # In-memory data store

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(list(products.values())), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    else:
        return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    product_id = len(products) + 1
    products[product_id] = {
        'id': product_id,
        'name': data['name'],
        'price': data['price']
    }
    return jsonify({'message': 'Product added successfully', 'id': product_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

