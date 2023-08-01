import requests
import time
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_firsturl(url,max_retries=5):
    for retry in range(max_retries):
        try: 
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad response codes (e.g., 404, 500)
            break  # If successful, break out of the retry loop
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if retry < max_retries - 1:
                print(f"Retrying in 5 seconds... (Attempt {retry + 2}/{max_retries})")
                time.sleep(5)
            else:
                print("Max retries reached. Exiting.")
                return None
    soup = BeautifulSoup(response.text, 'html.parser')
    first_product = soup.find("a", class_="a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal")
    
    if first_product is None:
        print("No products found.")
        return None

    href_value = first_product.get('href')
    result_url = "https://www.amazon.in" + href_value
    return result_url

if __name__ == "__main__":
    search_term = input("Enter your product name: ")
    url = f"https://www.amazon.in/s?k={search_term}"
    result = get_firsturl(url)
    if result:
        print("First product URL:", result)
    else:
        print("Product not found")    
