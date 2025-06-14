from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from db import *
import random as rnd
from scrape import *

#app config
app = Flask(__name__)
CORS(app)

#register endpoint
@app.route('/register', methods=['POST'])
def handle_register():
    user = request.json
    print(user)
    newUser = User(user['name'], user['email'])
    code = newUser.save()
    myUser = newUser.get_user_by_email()
    if (code == 'name-mismatch'):
        return jsonify({"error": "email was found, name did not match"})
    elif (code == 'login'):
        return jsonify({"login": "User Successfully Logged-in", "User": myUser})
    else:
        return jsonify({"register": "User Successfully Registered", "User": myUser})


@app.route('/scrape', methods=['GET'])
def handle_scrape():
    query = request.args.get('query')
    print(query)
    if (query != '' or query != None):
        return jsonify(scrape_products(query))

@app.route('/products', methods=['GET'])
def get_product_list():
    products = get_products()
    print(products[0])
    return jsonify(products)

if __name__ == '__main__':
   app.run(debug=True)