import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_item_details(driver, item_url):
    item_details = {}
    try:
        driver.get(item_url)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
        
        title = driver.find_element(By.CLASS_NAME, "title").text.strip()
        price = driver.find_element(By.CLASS_NAME, "price").text.strip()
        num_reviews = driver.find_element(By.CLASS_NAME, "ratings").text.strip()
        
        item_details['Title'] = title
        item_details['Price'] = price
        item_details['Number of Reviews'] = num_reviews
        
        print(f"Scraped item details for: {title}")
    except Exception as e:
        print(f"Failed to scrape item details for {item_url}: {str(e)}")
    return item_details

def save_to_file(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    item_links = [link['href'] for link in soup.find_all('a', class_='title')]

    driver = webdriver.Chrome()

    scraped_data = []

    for link in item_links:
        item_url = f"https://webscraper.io{link}"
        item_details = scrape_item_details(driver, item_url)
        scraped_data.append(item_details)

    driver.quit()

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





