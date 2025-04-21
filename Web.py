import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from twitterscrapping import main as scrape_data
from pymongo import MongoClient
import logging

load_dotenv(".env")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

client = MongoClient(os.getenv('MONGODB_URI'))
database = client.twitter_trends
trend_collection = database.trends

@app.route('/')
def home():
    trend_data = trend_collection.find(sort=[('date', -1)], projection={'_id': False})
    return render_template('index.html', trend=trend_data(0))

@app.route('/scrape', methods=['POST'])
def initiate_scrape():
    log.info("Scraping initiated")
    try:
        scrape_data()
        log.info("Scraping finished successfully")
    except Exception as error:
        log.error(f"Scraping error: {error}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)