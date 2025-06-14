from db import *
from scrape import *
from datetime import date

if __name__ == '__main__':
    with open('categoriesScraped.txt', 'r') as categories:
        for entry in categories:
            entry = entry.strip()
            #scrape the same category UNTIL output entries >= 5
            while True:
                output = scrape_products(entry)
                if (len(output) >= 5):
                    break



    #**emailer**
    #todaysDate = date.today().strftime("%m-%d")
    #userCollection, productCollection = connectToDB()
    #subscribedUsers = list(userCollection.find({'isSubscribed': True}, {'_id': 0}))
    #for user in subscribedUsers:
        #print(user)
        #try:
            #send_email('BestScrape', f'({todaysDate}) Daily Update', user['email'])
        #except Exception as e:
            #print(f'error sending email: {e}')