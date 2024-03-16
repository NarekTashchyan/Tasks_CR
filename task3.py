import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_item_details(driver, item_url):
    """
    Function to scrape details of an item using Selenium.
    
    Args:
    - driver: WebDriver instance.
    - item_url: URL of the item page.
    
    Returns:
    - item_details: Dictionary containing details of the item.
    """
    item_details = {}
    try:
        # Open the item page
        driver.get(item_url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        
        # Extract item details
        title = driver.find_element(By.CLASS_NAME, "title").text.strip()
        price = driver.find_element(By.CLASS_NAME, "price").text.strip()
        num_reviews = driver.find_element(By.CLASS_NAME, "ratings").text.strip()
        
        # Store item details in a dictionary
        item_details['Title'] = title
        item_details['Price'] = price
        item_details['Number of Reviews'] = num_reviews
        
        print(f"Scraped item details for: {title}")
    except Exception as e:
        print(f"Failed to scrape item details for {item_url}: {str(e)}")
    return item_details

def save_to_file(url):
    """
    Function to scrape item details from a given URL and save them to a file.
    
    Args:
    - url: URL of the page to scrape.
    """
    # Fetch the main URL using requests
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all item links on the main page
    item_links = [link['href'] for link in soup.find_all('a', class_='title')]

    # Initialize the WebDriver instance
    driver = webdriver.Chrome()

    # List to hold scraped item details
    scraped_data = []

    # Iterate through each item link and scrape details using Selenium
    for link in item_links:
        item_url = f"https://webscraper.io{link}"
        item_details = scrape_item_details(driver, item_url)
        scraped_data.append(item_details)

    # Close the browser window
    driver.quit()

    # Save the scraped data into a text file
    with open("data.txt", "a", encoding="utf-8") as file:
        for item in scraped_data:
            file.write(f"Title: {item.get('Title', '')}\n")
            file.write(f"Price: {item.get('Price', '')}\n")
            file.write(f"Number of Reviews: {item.get('Number of Reviews', '')}\n")
            file.write("\n")

def all_categories():
    """
    Function to scrape data from all categories.
    """
    main_url = 'https://webscraper.io/test-sites/e-commerce/allinone'
    save_to_file(main_url)
    categories = ['computers', 'phones']
    for category in categories:
        category_url = f'{main_url}/{category}'
        save_to_file(category_url)
        if category == 'computers':
            others = ['laptops', 'tablets']
            for other_c in others:
                save_to_file(f'{category_url}/{other_c}')
        elif category == 'phones':
            save_to_file(f'{category_url}/touch')
        
all_categories() 

print("Scraped data saved successfully.")





