from flask import Flask, request, jsonify

app = Flask(__name__)

orders = {}  # In-memory data store

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order_id = len(orders) + 1
    orders[order_id] = {
        'id': order_id,
        'product_id': data['product_id'],
        'user_id': data['user_id'],
        'quantity': data['quantity']
    }
    return jsonify({'message': 'Order created successfully', 'id': order_id}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    user_orders = [order for order in orders.values() if order['user_id'] == user_id]
    return jsonify(user_orders), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500
