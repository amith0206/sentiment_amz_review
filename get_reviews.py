import requests
from bs4 import BeautifulSoup
import time
import sentiment_analysis as analysis
import get_first_product_url as first_url
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_reviews(url, headers=headers, max_retries=20):
    if url is None:
        print("URL not found")
        exit()  # Corrected exit statement
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
    url = first_url.get_firsturl()
    rev_data = scrape_reviews(url)
    rev_result = []
    
    if rev_data:
        rev_result = [i.strip() for i in rev_data if i.strip()]
        with open("review_with_polarity.csv", 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Review', 'Polarity'])
            
            for line in rev_result:
                polarity = analysis.get_sentiment(line)
                csv_writer.writerow([line, polarity])
                
                print(f'Review: {line}')
                print(f'Polarity: {polarity}')
            
    else:
        print('Thank you')
        

    
