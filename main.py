from selenium import webdriver
from sqlalchemy import false
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json


with open("scraped.json", "w") as f:
    json.dump([], f)


def write_json(new_data, filename='scraped.json'):
    with open(filename, 'r+') as file:
        # load exising data into a dictionary
        file_data = json.load(file)
        # joins new data with old data
        file_data.append(new_data)
        # sets file current offset position to 0
        file.seek(0)
        # converts back to json
        json.dump(file_data, file, indent=4)


# Browser instance
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Url link
browser.get(
    'https://www.amazon.co.uk/s?k=iphone&crid=1CAM2HI01J907&sprefix=iphone%2Caps%2C310&ref=nb_sb_noss_1')
browser.find_element_by_id('sp-cc-accept').click()
isNextDisabled = False

while not isNextDisabled:
    try:
        # Wait to load elements 10 seconds after the Xpath value has been found
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@data-component-type="s-search-result"]')))
        # find elements and catch by div
        elem_list = browser.find_element_by_css_selector(
            "div.s-main-slot.s-result-list.s-search-results.sg-row")
        # elemet_items = browser.find by Xpath
        elem_items = browser.find_elements_by_xpath(
            '//*[@data-component-type="s-search-result"]')

        # create a for loop to get all 20 items from a page
        for x in elem_items:
            # use the .text to get all text from a tag
            product_title = x.find_element_by_tag_name('h2').text
            # use this data if no price is found
            product_price = 'No Price Found'
            # use this data if no image is found
            product_image = 'No image found'
            # fetch the product url
            product_url = x.find_element_by_class_name(
                'a-link-normal').get_attribute('href')

            # try this block of code, if there is any form of error, JUMP to PASS
            try:
                product_price = x.find_element_by_class_name(
                    'a-price').text.replace("\n", ".")
            except:
                pass
            # try this block of code, if there is any form of error, JUMP to PASS
            try:
                product_image = x.find_element_by_class_name(
                    's-image').get_attribute('src')
            except:
                pass
            # Print the results
            print('Product Title:', product_title)
            print('Product Price:', product_price)
            print('Product Image URL:', product_image)
            print('Product Link:', product_url)
            print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------')

            write_json({"title": product_title,
                       "price": product_price,
                       "image":product_image,
                       "link":product_url})

        # While waiting for next page to load
        button_click = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 's-pagination-next')))
        # Check for the next page instance
        next_class = button_click.get_attribute('class')
        print(next_class)
        # check if a keyword exist in the class attribute
        if 'disabled' in next_class:
            isNextDisabled = True
        else:
            browser.find_element_by_class_name('s-pagination-next').click()
    except Exception as e:
        print(e, 'Error')
