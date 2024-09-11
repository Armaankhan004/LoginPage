from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(24)  # For session management

# In-memory user database (replace with a real database in production)
users = {
    "user@example.com": generate_password_hash("password123")
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username not in users:
        return jsonify({"message": "User not found"}), 404

    if check_password_hash(users[username], password):
        session['user'] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logout successful"}), 200

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user' in session:
        return jsonify({"message": "User is logged in", "user": session['user']}), 200
    else:
        return jsonify({"message": "User is not logged in"}), 401

if __name__ == '__main__':
    app.run(debug=True)