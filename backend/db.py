from dotenv import load_dotenv
import os
from datetime import date
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random

def connectToDB():
    load_dotenv('../secrets.env')
    uri = os.getenv("CONNECTION_STRING")

    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Successfully connected to DB")
    except Exception as e:
        print(e)

    db = client.get_database('BestScrape')
    userCollection = db.get_collection('users')
    productCollection = db.get_collection('products')

    return userCollection, productCollection

class User:
    #User class constructor
    def __init__(self, name, email):
        self.userid = generate_unique_userid()
        self.name = name
        self.email = email
        self.isSubscribed = False

    
    #saves the user to DB
    #
    def save(self):
        duplicate = userCollection.find_one({
            'email': self.email.lower()
        })
        if (duplicate is None):
            userCollection.insert_one({
                'userid': self.userid,
                'name': self.name.lower(),
                'email': self.email,
                'isSubscribed': self.isSubscribed
            })
            newUser = userCollection.find_one({
                'email': self.email.lower()
            })
            return 'register', {key: value for key, value in newUser.items() if key != '_id'}
        else:
            if (duplicate['name'] == self.name.lower()):
                return 'login', {key: value for key, value in duplicate.items() if key != '_id'}
            else:
                return 'name-mismatch', None
    
    #Gets the user by email
def get_user_by_id(userid):
    print(f'userid: {userid}')
    user = userCollection.find_one({
        'userid': int(userid)
    })
    print(f'user found: {user}')
    if (user == None):
        print('user could not be found')
        return None

    filteredUser = {key: value for key, value in user.items() if key != '_id'}
    return filteredUser

def subscribe_user(userid):
    user = userCollection.update_one(
        {'userid': int(userid)},
        {'$set': {'isSubscribed': True}}
    )
    print(f'user found when subscring: {user}')
    return {'success': 'user Successfully subscribed!'}

def unsubscribe_user(userid):
    user = userCollection.update_one(
        {'userid': userid},
        {'$set': {'isSubscribed': False}}
    )


class Product:
    def __init__(self, title, category, price, SKU, imgSrc):
        self.title = title
        self.category = category
        self.price = price
        self.SKU = SKU
        self.imgSrc = imgSrc
    
    def save(self):
        todaysDate = date.today().strftime("%m-%d")
        duplicate = productCollection.find_one({
            'SKU': self.SKU
        })
        #if there is no duplicate, add to DB
        if (duplicate is None):
            productCollection.insert_one({
                'title': self.title,
                'category': self.category,
                'price': float(self.price),
                'price_history': [f'{todaysDate}={self.price}'],
                'SKU': self.SKU,
                'imgSrc': self.imgSrc
            })
        else:
        #if product already in DB, set price field and add a new price-history node at head
            if ((self.price > duplicate.get('price'))):
                productCollection.update_one(
                    {'_id': duplicate.get('_id', 'old price not found')},
                    {"$set": {'price': self.price, 'direction': 'increase'}}
                )
                productCollection.update_one(
                    {'SKU': self.SKU},
                    {
                        "$push": {
                            "price_history": {
                                "$each": [f'{todaysDate}={self.price}'],
                                "$position": 0
                            }
                        }
                    }
                )
            elif ((self.price < duplicate.get('price'))):
                productCollection.update_one(
                    {'_id': duplicate.get('_id', 'old price not found')},
                    {"$set": {'price': self.price, 'direction': 'decrease'}}
                )
                productCollection.update_one(
                    {'SKU': self.SKU},
                    {
                        "$push": {
                            "price_history": {
                                "$each": [f'{todaysDate}={self.price}'],
                                "$position": 0
                            }
                        }
                    }
                )


#returns a list of the products DB
def get_products():
    allProducts = list(productCollection.find())
    filteredProducts = []
    for product in allProducts:
        filteredProduct = {key: value for key, value in product.items() if key != '_id'}
        filteredProducts.append(filteredProduct)
    return filteredProducts

def generate_unique_userid():
    while True:
        candidate_id = random.randint(1000, 9999)
        # Check if this ID already exists
        if not userCollection.find_one({"userid": candidate_id}):
            return candidate_id


userCollection, productCollection = connectToDB()