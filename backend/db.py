from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class User:
    #User class constructor
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    #returns True if success, False if email already found in DB
    def save(self):
        duplicate = userCollection.find_one({
            'email': self.email.lower()
        })
        if (duplicate is None):
            userCollection.insert_one({
                'name': self.name.lower(),
                'email': self.email
            })
            return 'register'
        else:
            if (duplicate['name'] == self.name):
                return 'login'
            else:
                return 'name-mismatch'
    
    #Gets the 
    def get_user_by_email(self):
        user = userCollection.find_one({
            'email': self.email.lower()
        })
        filteredUser = {key: value for key, value in user.items() if key != '_id'}
        return filteredUser

class Product:
    def __init__(self, title, price, SKU, imgSrc):
        self.title = title
        self.price = price
        self.SKU = SKU
        self.imgSrc = imgSrc
    
    def save(self):
        duplicate = productCollection.find_one({
            'SKU': self.SKU
        })
        if (duplicate is None):
            productCollection.insert_one({
                'title': self.title,
                'price': self.price,
                'SKU': self.SKU,
                'imgSrc': self.imgSrc
            })

def get_products():
    allProducts = list(productCollection.find())
    filteredProducts = []
    for product in allProducts:
        filteredProduct = {key: value for key, value in product.items() if key != '_id'}
        filteredProducts.append(filteredProduct)

    return filteredProducts

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

