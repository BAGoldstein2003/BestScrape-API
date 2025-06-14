from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlencode
from db import *

def newslow_scroll_to_bottom(driver, pause_time=1, scroll_step=500, max_tries=5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    tries = 0

    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            tries += 1
            if tries >= max_tries:
                break  # No more content after several tries
        else:
            tries = 0  # Reset if new content was loaded

        last_height = new_height

def scrape_products(searchItem):
    query = urlencode({"st": searchItem})
    options = Options()
    url = f"https://www.bestbuy.com/site/searchpage.jsp?{query}"
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)
    newslow_scroll_to_bottom(driver, pause_time=.4, scroll_step=300, max_tries=3)
    products = driver.find_elements(By.CLASS_NAME, 'product-list-item')
    productList = []
    
    #grab products on the page
    for idx, product in enumerate(products):
        try:
            #try to grab title and price
            productTitle = product.find_element(By.TAG_NAME, 'h2').text
            productPrice = product.find_element(By.CLASS_NAME, 'customer-price').text
            productImageSrc = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
            
            #try to grab SKU
            skuElements = product.find_elements(By.XPATH, ".//div[contains(text(), 'SKU:')]")
            for el in skuElements:
                text = el.text
                if "SKU:" in text:
                    productSKU = text.split('SKU: ')[1]
                    break

            productList.append(
                {
                    'productTitle': productTitle,
                    'productPrice': productPrice,
                    'productSKU': productSKU,
                    'productImageSrc': productImageSrc
                }
            )
        except:
            print(f"Product {idx} has no h2 tag")
        
    driver.close()

    #add products to DB
    for product in productList:
        productObj = Product(product['productTitle'], product['productPrice'], product['productSKU'], product['productImageSrc'])
        productObj.save()
    print(productList)
    print(f'{len(productList)} products scraped')
    return productList