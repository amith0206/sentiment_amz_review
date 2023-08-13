import requests
from bs4 import BeautifulSoup
import time
import get_first_product_url as p
import sentiment_analysis as q

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_reviews(url, headers=headers, max_retries=10):
    if url is None:
        print("URL not found")
        return None

    data_str = ""  # Initialize data_str to store review text
    print("Searching for reviews")
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

    soup = BeautifulSoup(response.content, "html.parser")
    review_texts = soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")

    for item in review_texts:
        data_str = data_str + item.get_text()

    result = data_str.split("\n")
    return result

if __name__ == "__main__":
    url = p.get_firsturl()
    rev_data = scrape_reviews(url)
    rev_result=[]
    if(rev_data):
        for i in rev_data:
            if i=="":
                pass
            else:
                rev_result.append(i)
    else:
        print('Thank you')    
        

    
