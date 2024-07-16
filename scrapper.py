from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np

#Array where the product IDs will be stored
idProducts = []

#Array where the product data will be stored
data = np.empty((0, 5), dtype=object)

#Start the search engine
opt = Options()
opt.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36")
opt.add_argument('--headless')

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options=opt
)


def ScrapItem(id):
    # We define a function that will go to the url of each product that we put as a parameter, 
    # and will extract the title, the ratings, the price, and the products sold.
    global data
    print('Start send: ',id)
    driver.get(f'https://es.aliexpress.com/item/{id}.html')
    title = driver.find_elements(By.XPATH, "//h1")
    reviews = driver.find_elements(By.XPATH, "//div[@data-pl='product-reviewer']//a")
    ships = driver.find_elements(By.XPATH, "//div[@data-pl='product-reviewer']//span")
    price = driver.find_elements(By.XPATH, "//div[@data-pl='product-price']//span")

    print('----------------------------------------------------------------')
    vTitle = title[0].text
    vReviews = reviews[0].text
    
    vShip = ''
    for s in ships:
        if('vendido' in s.text):
            vShip = s.text
            
    vPrice = ''
    for p in price:
        if('price--originalText--' in p.get_attribute('class')):
            vPrice = p.text
            
    print("Title: ", vTitle)
    print("Reviews: ", vReviews)
    print("Ships: ", vShip)
    print("Price: ", vPrice)
    #Add the data obtained to the array
    data = np.append(data, [[id, vTitle, vReviews, vShip, vPrice]], axis=0)

print('--------------------------------------------------------------------------')
#Go to the url where the best aliexpress products are
driver.get("https://www.aliexpress.com/gcp/300001064/aptaxwR82N")
#Extract the div of each product
products = driver.find_elements(By.XPATH, '//div[@style="border-radius: 16px;"]//a')
print('--------------------------------------------------------------------------')
#It searches between products to extract their ID
for product in products:
    idProducts.append(product.get_attribute('id'))

print(idProducts)
for idP in idProducts:
    ScrapItem(idP)

print(data)
#The data obtained is printed.
np.savetxt('bestProducts.csv', data, delimiter=',')