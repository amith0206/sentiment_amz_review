import requests
from bs4 import BeautifulSoup

def get_amazon_reviews(product_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response codes (e.g., 404, 500)

        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = []
        review_elements = soup.find_all('div', {'data-hook': 'review'})
        for review_element in review_elements:
            rating_element = review_element.find('i', {'data-hook': 'review-star-rating'})
            if rating_element:
                rating = float(rating_element.text.split()[0])
            else:
                rating = None

            text_element = review_element.find('span', {'data-hook': 'review-body'})
            if text_element:
                review_text = text_element.text.strip()
            else:
                review_text = None

            reviews.append({'rating': rating, 'text': review_text})

        return reviews
    except requests.RequestException as e:
        print("Error during HTTP request:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def get_product_url_by_keyword(search_keyword):
    try:
        search_url = f'https://www.amazon.com/s?k={search_keyword}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response codes (e.g., 404, 500)

        soup = BeautifulSoup(response.text, 'html.parser')
        first_product_element = soup.find('a', {'class': 'a-link-normal', 'data-component-type': 's-product-image'})

        if first_product_element:
            product_url = first_product_element['href']
            return f'https://www.amazon.com{product_url}'
        else:
            print("No product found for the given keyword.")
            return None
    except requests.RequestException as e:
        print("Error during HTTP request:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    search_keyword = input('Enter your product name here : ')
    product_url = get_product_url_by_keyword(search_keyword)

    if product_url:
        product_reviews = get_amazon_reviews(product_url)
        if product_reviews:
            for idx, review in enumerate(product_reviews, start=1):
                print(f"Review {idx}")
                print(f"Rating: {review['rating']}")
                print(f"Text: {review['text']}")
                print("------------------------")
  
     
