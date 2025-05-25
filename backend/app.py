from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from db import *
from emailer import *
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
    status, user = newUser.save()
    print(user)
    
    if (status == 'name-mismatch'):
        return jsonify({"error": "email was found, name did not match"})
    elif (status == 'login'):
        return jsonify({"login": "User Successfully Logged-in", "User": user})
    elif (status == 'register'):
        return jsonify({"register": "User Successfully Registered", "User": user})
    
@app.route('/subscribe', methods=['GET'])
def handle_subscribe():
    userId = request.args.get('userid')
    userEmail = request.args.get('useremail')
    user = get_user_by_id(userId)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    email = user.get('email')
    print(f'subscriber email: {email}')
    subscribe_user(userId)
    try:
        send_email('BestScrape', 'Thanks for Subscribing to our service!', userEmail)
    except:
        return {'error': 'could not send email'}
    return {'success': 'email successfully sent to brianalexgoldstein@gmail.com'}
    
    


@app.route('/scrape', methods=['GET'])
def handle_scrape():
    query = request.args.get('query')
    userid = request.args.get('userid')
    if (query != '' or query != None):
        return jsonify(scrape_products(query, userid))

@app.route('/products', methods=['GET'])
def get_product_list():
    products = get_products()
    return jsonify(products)


if __name__ == '__main__':
   app.run(debug=True)