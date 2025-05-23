# Twitter Trending Topics Scraper Report

## Project Overview

This project involves a Python-based web scraping application that uses Selenium to read Twitter’s homepage and extract the top 5 trending topics from the "What’s Happening" section. The scraped data is stored in a MongoDB database and can be viewed through a Flask web interface.

## Technologies Used

1. **Selenium**: Automates web browser actions to scrape data from Twitter.
2. **MongoDB**: Stores the scraped trending topics.
3. **Flask**: Provides a web interface to trigger scraping and display data.
4. **Python-Dotenv**: Manages environment variables securely.
5. **BeautifulSoup**: Parses HTML content to extract trending topics.

## Key Features

1. **Automated Web Scraping**: Uses Selenium and BeautifulSoup to gather real-time trending topics from Twitter.
2. **MongoDB Integration**: Stores the extracted trending topics for future reference.
3. **Flask Web Interface**: Allows users to trigger the scraping process and view the collected data.

## Installation Instructions

### Prerequisites

- Python 3.x
- MongoDB
- ChromeDriver

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/RK02k/Twitter-Scrapping-using-selenium.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd twitter-scraping-app
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the project directory and add the necessary credentials:
    ```makefile
    proxymesh_user=your_proxymesh_username
    proxymesh_pass=your_proxymesh_password
    X_EMAIL=your_twitter_email
    X_PASS=your_twitter_password
    X_USER=your_twitter_username
    MONGODB_URI=your_mongodb_uri
    ```

## Usage

1. **Run the Flask application**:
    ```bash
    python Web.py
    ```

2. **Access the web interface**:
    Open your web browser and go to `http://localhost:5000`.

3. **Trigger the scraping process**:
    Click the "Scrape Data" button to start scraping Twitter for trending topics.

4. **View the results#   t w i t t e r - s c r a p p e r  
 