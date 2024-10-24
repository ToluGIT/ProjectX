from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)

users = {}  # In-memory data store for simplicity

@app.route('/users/register', methods=['POST'])
def register_user():
    """Register a new user."""
    logging.info('Register user called')

    data = request.json
    user_id = len(users) + 1
    hashed_password = generate_password_hash(data['password'], method='sha256')

    users[user_id] = {
        'id': user_id,
        'username': data['username'],
        'password': hashed_password
    }

    return jsonify({'message': 'User registered successfully', 'id': user_id}), 201

@app.route('/users/login', methods=['POST'])
def login_user():
    """Authenticate user login."""
    data = request.json
    for user in users.values():
        if user['username'] == data['username'] and check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Login successful', 'id': user['id']}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve user details."""
    user = users.get(user_id)
    if user:
        return jsonify({'id': user['id'], 'username': user['username']}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
