from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import importlib
import time
import io
import os
import sys
import random

f = io.open(os.path.join(os.path.dirname(sys.executable), file_out), 'w', encoding='utf-8')
global config
config = importlib.load_source('data', '', f)
f.close()

if config.headless:
    options = Options()
    options.headless = True

    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # driver

else:
    browser = webdriver.Chrome(ChromeDriverManager().install()) # driver

# This function handles dynamic page content loading using Selenium
def tweet_scroller(url):
    browser.get(url)

    last_height = browser.execute_script('return document.body.scrollHeight')

    page_count = config.pages

    while page_count > 0:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        # Define how many seconds to wait while dynamic page content loads
        time.sleep(3)
        new_height = browser.execute_script('return document.body.scrollHeight')

        if new_height == last_height:
            break
        else:
            last_height = new_height

        page_count -= 1

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

# Function to read config txt file and return scroll time settings
def config_reader():

    configuration = yaml.safe_load(open(os.path.join(os.path.dirname(sys.executable), 'config.txt'), 'r'))


    # main
if __name__ == "__main__":
    html = tweet_scroller(url_selector())
    txt_writer(html)
    browser.quit()