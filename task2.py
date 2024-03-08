import requests
from bs4 import BeautifulSoup


def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        product_cards = soup.find_all('div', class_='thumbnail')

        products_info = []

        for card in product_cards:
            product_name = card.find('a', class_='title').text.strip()

            review_element = card.find('p', class_='float-end review-count')
            num_reviews = review_element.text.strip() if review_element else 'No reviews'

            price_element = card.find('h4', class_='pull-right')
            price = price_element.text.strip() if price_element else 'Price not available'

            description_element = card.find('p', class_='description card-text')
            description = description_element.text.strip() if description_element else 'description not available'
            
            products_info.append({'Name': product_name, 'Reviews': num_reviews, 'Price': price, 'Description': description})

        return products_info

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to {url}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_data_to_file(products_info):
    try:
        with open('data.txt', 'w', encoding='utf-8') as file:
            for product in products_info:
                file.write(f"Name: {product['Name']}\n")
                file.write(f"Description: {product['Description']}\n")
                file.write(f"Price: {product['Price']}\n")
                file.write(f"Reviews: {product['Reviews']}\n")
                file.write("=" * 50 + "\n")
        print("Scraped data saved successfully to data.txt")
    except Exception as e:
        print(f"An error occurred while saving data to file: {e}")


def main():
    url = 'https://webscraper.io/test-sites/e-commerce/allinone'
    products_info = scrape_data(url)
    if products_info:
        save_data_to_file(products_info)


main()
