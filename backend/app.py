from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from db import *
import random as rnd

#app config
app = Flask(__name__)
CORS(app)

#register endpoint
@app.route('/register', methods=['POST'])
def handle_register():
    user = request.json
    print(user)
    newUser = User(user['name'], user['email'])
    status, user = newUser.save()
    print(user)
    
    if (status == 'name-mismatch'):
        return jsonify({"error": "email was found, name did not match"})
    elif (status == 'login'):
        return jsonify({"login": "User Successfully Logged-in", "User": user})
    elif (status == 'register'):
        return jsonify({"register": "User Successfully Registered", "User": user})

@app.route('/products', methods=['GET'])
def get_product_list():
    products = get_products()
    return jsonify(products)


if __name__ == '__main__':
   app.run(debug=True)