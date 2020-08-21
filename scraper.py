from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import io
import os
import sys
import random

browser = webdriver.Chrome(ChromeDriverManager().install())  # driver

# This function handles dynamic page content loading using Selenium
def tweet_scroller(url):
    browser.get(url)

    last_height = browser.execute_script('return document.body.scrollHeight')

    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # Define how many seconds to wait while dynamic page content loads
        time.sleep(3)
        new_height = browser.execute_script('return document.body.scrollHeight')

        if new_height == last_height:
            break
        else:
            last_height = new_height

    page_html = browser.page_source

    return page_html


# Function to write txt file
def txt_writer(target_html):
    file_out = 'webreturn.txt'

    with io.open(os.path.join(os.path.dirname(sys.executable), file_out), 'w', encoding='utf-8') as txtfile:
        txtfile.write(target_html)

# Function to read urls txt file and randomly select a url for handling
def url_selector():

    url_collection = open(os.path.join(os.path.dirname(sys.executable), 'URLs.txt'), 'r')
    lines = url_collection.readlines()

    return random.choice(lines)

    # main
if __name__ == "__main__":
    html = tweet_scroller(url_selector())
    txt_writer(html)
    browser.quit()