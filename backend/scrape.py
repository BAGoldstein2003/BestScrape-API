from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlencode
from db import *

def iterative_scroll_until_min_items(driver: webdriver.Chrome, min_items=12, scroll_step=500, pause_time=0.5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        items = driver.find_elements(By.CLASS_NAME, 'product-list-item')
        productNames = driver.find_elements(By.TAG_NAME, 'h2')
        if new_height == last_height and len(productNames) >= min_items:
            break
        last_height = new_height

def scroll_by_step(driver: webdriver.Chrome, stepSize = 300):
    driver.execute_script(f"window.scrollBy(0, {stepSize});")

def is_bottom_of_screen(driver: webdriver.Chrome):
    isAtBottom = bool(driver.execute_script("""
        return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;
    """))
    return isAtBottom

def scrape_products(searchItem):
    query = urlencode({"st": searchItem})
    options = Options()
    url = f"https://www.bestbuy.com/site/searchpage.jsp?{query}"
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)
    iterative_scroll_until_min_items(driver)
    products = driver.find_elements(By.CLASS_NAME, 'product-list-item')
    productList = []
    print(len(products))
    
    #grab products on the page
    for idx, product in enumerate(products):
        try:
            #try to grab title, price, and Image Source
            productTitle = product.find_element(By.CLASS_NAME, 'product-title').text
            print(f'Product {idx} Title: {productTitle}')
            productPrice = product.find_element(By.CLASS_NAME, 'customer-price').text
            print(f'Product {idx} Price: {productPrice}')
            productImageSrc = product.find_element(By.TAG_NAME, 'img').get_attribute('src')
            print(f'Product {idx} Image Source: {productImageSrc}')

            #try to grab SKU
            skuElements = product.find_elements(By.XPATH, ".//div[contains(text(), 'SKU:')]")
            for el in skuElements:
                text = el.text
                if "SKU:" in text:
                    productSKU = text.split('SKU: ')[1]
                    print(f'Product SKU: {productSKU}')
                    break
            
            #append findings to product list
            productList.append(
                {
                    'productTitle': productTitle,
                    'productCategory': searchItem,
                    'productPrice': productPrice,
                    'productSKU': productSKU,
                    'productImageSrc': productImageSrc
                }
            )
        except Exception:
            print(f"Product {idx} was unable to be scraped")
        
    driver.close()

    #add products to DB
    for product in productList:
        productObj = (Product(product['productTitle'], product['productCategory'], 
                        float(product['productPrice'].replace(',', '')[1:]), 
                        product['productSKU'], product['productImageSrc'])
                     )
        productObj.save()
    print(f'{len(productList)} products scraped')
    print(productList)
    return productList

def scrape_amazon_product_deals():
    
    #helper function to remove duplicates from list
    def remove_duplicates_from_list(lst):
        seen = set()
        unique = []
        for d in lst:
            tup = tuple(sorted(d.items()))
            if tup not in seen:
                seen.add(tup)
                unique.append(d)
        return unique
    
    productList = []
    options = Options()
    url = f"https://www.amazon.com/deals?ref_=nav_cs_gb"
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url)
    
    #while there is still page left to scroll, scrape products and get their titles and images
    while (not is_bottom_of_screen(driver)): 
        productElements = driver.find_elements(By.CLASS_NAME, 'ProductCard-module__card_uyr_Jh7WpSkPx4iEpn4w')
        for idx, productElement in enumerate(productElements):
            try:
                productTitle = productElement.find_element(By.TAG_NAME, 'img').get_attribute('alt')
                productImageSrc = productElement.find_element(By.TAG_NAME, 'img').get_attribute('src')
                productLink = productElement.find_element(By.TAG_NAME, 'a').get_attribute('href')
                productDiscountAmount = productElement.find_elements(By.CLASS_NAME, 'a-size-mini')[0].text
                productDiscountType = productElement.find_elements(By.CLASS_NAME, 'a-size-mini')[1].text

                productList.append({
                    'productTitle': productTitle,
                    'productImageSrc': productImageSrc,
                    'productDiscount': f'{productDiscountType}: {productDiscountAmount}'
                })
            except Exception:
                print(f'couldnt retain title or image source of product {idx}')
        scroll_by_step(driver, stepSize = 900)
        time.sleep(1)
    return remove_duplicates_from_list(productList)
    
print(f'{len(scrape_amazon_product_deals())} amazon products scraped')