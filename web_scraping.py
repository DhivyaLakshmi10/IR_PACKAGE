import requests
from bs4 import BeautifulSoup
import csv

def get_amazon_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', class_='a-section review aok-relative')

        all_reviews = []

        for review in reviews:
            review_dict = {}
            # Extracting reviewer name
            reviewer_name = review.find('span', class_='a-profile-name')
            if reviewer_name:
                review_dict['Reviewer'] = reviewer_name.text.strip()

            # Extracting review title
            review_title = review.find('a', class_='review-title-content')
            if review_title:
                review_dict['Title'] = review_title.text.strip()

            # Extracting review rating
            review_rating = review.find('i', class_='review-rating')
            if review_rating:
                review_dict['Rating'] = review_rating.text.strip()

            # Extracting review content
            review_content = review.find('span', class_='review-text-content')
            if review_content:
                review_dict['Content'] = review_content.text.strip()

            all_reviews.append(review_dict)

        return all_reviews
    else:
        print("Failed to retrieve page:", response.status_code)
        return None

def save_reviews_to_csv(reviews, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Reviewer', 'Title', 'Rating', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)

if __name__ == "__main__":
    amazon_url = 'https://www.amazon.com/s?k=electronics'
    reviews = get_amazon_reviews(amazon_url)
    if reviews:
        save_reviews_to_csv(reviews, 'https://www.amazon.com/s?k=electronics')
        print("Reviews saved successfully.")
