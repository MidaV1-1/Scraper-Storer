# Import necessary packages
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up Chrome options to use the correct user profile
chrome_options = webdriver.ChromeOptions()

# Specify the correct user data directory and profile
chrome_options.add_argument("--user-data-dir=/mnt/c/Users/mida/AppData/Local/Google/Chrome/User Data")  # Path to user data
chrome_options.add_argument("--profile-directory=Default")  # Change to the profile you're signed in with, e.g., "Default", "Profile 1", etc.

# Initialize WebDriver with ChromeDriverManager and Chrome options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the Amazon review page
reviews_url = 'https://www.amazon.ae/KAREZZ-Ceremonial-Uji-Kyoto-Certified-Antioxidants/product-reviews/B0CZF1Z8PY/'

# Function to handle login (manual login if not already logged in)
def login_amazon():
    driver.get("https://www.amazon.ae/ap/signin")
    time.sleep(2)
    
    # Check if we're already logged in by looking for a sign-out button
    try:
        sign_in_button = driver.find_element(By.ID, 'signInSubmit')
        if sign_in_button.is_displayed():
            print("Not logged in. Please log in manually...")
            print("The script will pause for you to log in.")
            time.sleep(60)  # Pause for 1 minute, you can adjust this time
        else:
            print("Already logged in.")
    except Exception as e:
        print("Error during login:", e)

# Function to fetch review HTML from Amazon page
def reviewsHtml(url):
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    # Use BeautifulSoup to scrape the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    reviews = soup.find_all('div', {'data-asin': True})

    all_reviews = []
    for review in reviews:
        try:
            review_text = review.find('span', {'data-asin': True}).text.strip()
            review_date = review.find('span', {'class': 'a-size-base a-color-secondary review-date'}).text.strip()
            reviewer_name = review.find('span', {'class': 'a-profile-name'}).text.strip()
            all_reviews.append({'Review': review_text, 'Date': review_date, 'Reviewer': reviewer_name})
        except AttributeError:
            continue
    return all_reviews

# Login to Amazon (if needed)
login_amazon()

# Fetch reviews data
reviews_data = reviewsHtml(reviews_url)

# Convert reviews to a DataFrame
df = pd.DataFrame(reviews_data)

# Save reviews to a CSV file
df.to_csv('amazon_reviews.csv', index=False)

# Close the browser
driver.quit()

print("Successfully fetched and saved the reviews!")
