from db import *
from scrape import *
from datetime import date
from emailer import *

if __name__ == '__main__':
    with open('categoriesScraped.txt', 'r') as categories:
        for entry in categories:
            entry = entry.strip()
            scrape_products(entry)



    todaysDate = date.today().strftime("%m-%d")
    print(todaysDate)

    userCollection, productCollection = connectToDB()
    subscribedUsers = list(userCollection.find({'isSubscribed': True}, {'_id': 0}))
    for user in subscribedUsers:
        print(user)
        try:
            send_email('BestScrape', f'({todaysDate}) Daily Update', user['email'])
        except Exception as e:
            print(f'error sending email: {e}')