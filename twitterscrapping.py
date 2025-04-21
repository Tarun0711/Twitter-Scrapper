import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
from pymongo import MongoClient
import datetime
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv(".env")

proxy_user = os.getenv('proxymesh_user')
proxy_pass = os.getenv('proxymesh_pass')

twitter_email = os.getenv('X_EMAIL')
twitter_password = os.getenv('X_PASS')
twitter_user = os.getenv('X_USER')

mongo_client = MongoClient(os.getenv('MONGODB_URI'))
db_instance = mongo_client.twitter_trends
trends_collection = db_instance.trends

def fetch_proxy():
    return f"http://{proxy_user}:{proxy_pass}@us-ca.proxymesh.com:31280"

def setup_driver(proxy_address):
    chrome_opts = Options()
    chrome_opts.add_argument('--headless')
    chrome_opts.add_argument('--disable-gpu')
    chrome_opts.add_argument('--no-sandbox')
    chrome_opts.add_argument('--disable-dev-shm-usage')
    chrome_opts.add_argument('--disable-web-security')
    chrome_opts.add_argument("--start-maximized")
    chrome_opts.binary_location = "/usr/local/bin/chrome/opt/google/chrome/chrome"
    
    if proxy_address:
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = proxy_address
        proxy.ssl_proxy = proxy_address
        
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['proxy'] = proxy.to_capabilities()
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
    else:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
    
    return browser

def twitter_sign_in(browser):
    browser.get('https://x.com/login')
    time.sleep(5)
    email_field = browser.find_element(By.CSS_SELECTOR, "[name='text']")
    email_field.send_keys(twitter_user)
    time.sleep(1)
    email_field.send_keys(Keys.ENTER)
    time.sleep(4)
    password_field = browser.find_element(By.CSS_SELECTOR, "[name='password']")
    password_field.send_keys(twitter_password)
    time.sleep(1)
    password_field.send_keys(Keys.ENTER)
    time.sleep(4)

def fetch_trends(browser):
    browser.get('https://x.com/home')
    time.sleep(6)
    trends_list = []
    page_content = browser.page_source
    parsed_content = BeautifulSoup(page_content, 'html.parser')

    trend_elements = parsed_content.find_all('div', {'data-testid': 'trend'})

    for trend in trend_elements:
        trend_spans = trend.find_all('span')
        if trend_spans:
            trends_list.append(trend_spans[1].text)
    
    return trends_list

def retrieve_current_ip():
    proxy_url = "http://us-ca.proxymesh.com:31280"
    response = requests.get('http://httpbin.org/ip', proxies={'http': proxy_url, 'https': proxy_url}, auth=(proxy_user, proxy_pass))
    return response.json()['origin']

def save_trends_to_db(trends):
    trend_data = {
                'trend_1': trends[0],
                'trend_2': trends[1],
                'trend_3': trends[2],
                'trend_4': trends[3],
                'trend_5': trends[4],
                'timestamp': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'ip_address': retrieve_current_ip()
            }
    trends_collection.insert_one(trend_data)

def main_task():
    proxy_ip = fetch_proxy()
    browser = setup_driver(proxy_ip)
    try:
        twitter_sign_in(browser)
        trends = fetch_trends(browser)
        save_trends_to_db(trends)
    except Exception as error:
        print('An error occurred: ', error)
    finally:
        browser.quit()

if __name__ == "__main__":
    main_task()