import requests

def fetch(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to {url}: {e}")
        return None
    
print(fetch('https://hy.wikipedia.org/wiki/%D4%B1%D5%B6%D5%A4%D6%80%D5%A1%D5%B6%D5%AB%D5%AF_%D5%95%D5%A6%D5%A1%D5%B6%D5%B5%D5%A1%D5%B6'))
