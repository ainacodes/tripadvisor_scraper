import requests
from bs4 import BeautifulSoup
import logging
import csv
import time


def setup_request():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    proxies = {
        'http': 'http://username:password@host:port',
        'https': 'http://username:password@host:port'
    }

    return headers, proxies


def get_restaurant_info(soup):
    restaurant_info = {
        'name': '',
        'price_level': '',
        'cuisine_type': '',
        'total_rating': '',
        'total_reviews': '',
        'food_rating': '',
        'service_rating': '',
        'value_rating': '',
        'atmosphere_rating': '',
        'ranking': '',
        'city': '',
        'address': '',
        'phone_no': ''
    }

    restaurant_info['name'] = soup.find('h1').text.strip()

    # General info processing
    general_infos = soup.find('span', class_='cPbcf').text.strip()
    info_parts = general_infos.split(', ')
    restaurant_info['price_level'] = info_parts[0]
    restaurant_info['cuisine_type'] = ', '.join(info_parts[1:])

    # Rating and review info
    detail_cards = soup.find_all(
        'div', attrs={'data-automation': 'OVERVIEW_TAB_ELEMENT'})
    if detail_cards:
        rating_info = detail_cards[0]
        restaurant_info['total_rating'] = rating_info.find(
            'span', class_='biGQs').text.strip()
        reviews_text = rating_info.find('div', class_='jXaJR').text.strip()
        restaurant_info['total_reviews'] = reviews_text.replace(' reviews', '')

        # Detailed ratings
        try:
            rating_container = rating_info.find('div', class_='khxWm')
            if rating_container:
                rating_category = rating_container.find_all(
                    'div', class_='YwaWb')
                if len(rating_category) >= 4:
                    restaurant_info['food_rating'] = rating_category[0].find(
                        'svg', class_='UctUV').find('title').text.strip().replace(' of 5 bubbles', '')
                    restaurant_info['service_rating'] = rating_category[1].find(
                        'svg', class_='UctUV').find('title').text.strip().replace(' of 5 bubbles', '')
                    restaurant_info['value_rating'] = rating_category[2].find(
                        'svg', class_='UctUV').find('title').text.strip().replace(' of 5 bubbles', '')
                    restaurant_info['atmosphere_rating'] = rating_category[3].find(
                        'svg', class_='UctUV').find('title').text.strip().replace(' of 5 bubbles', '')
        except Exception as e:
            logging.error(f"Error extracting detailed ratings: {str(e)}")

        # Ranking and city info
        ranking_tag = rating_info.find_all('a', class_='BMQDV')
        if len(ranking_tag) > 1:
            ranking_text = ranking_tag[1].find('span').text.strip()
            restaurant_info['ranking'] = ranking_text.split()[
                0].replace('#', '')
            in_index = ranking_text.split().index('in')
            restaurant_info['city'] = ' '.join(
                ranking_text.split()[in_index + 1:])

    # Address and phone info
    if len(detail_cards) > 2:
        location_info = detail_cards[2]
        restaurant_info['address'] = location_info.find(
            'span', class_='biGQs').text.strip()

        # Phone number
        try:
            phone_link = location_info.find('a', attrs={'aria-label': 'Call'})
            if phone_link:
                restaurant_info['phone_no'] = phone_link.get(
                    'href').replace('tel:', '')
        except Exception as e:
            logging.error(f"Error extracting phone number: {str(e)}")

    return restaurant_info


def scrape_reviews(soup):
    reviews = []
    review_cards = soup.find_all(
        'div', attrs={'data-automation': 'reviewCard'})

    for review in review_cards:
        review_data = {
            'rating': '',
            'title': '',
            'text': '',
            'date': ''
        }

        rating_element = review.find('svg', class_='UctUV')
        if rating_element:
            review_data['rating'] = rating_element.find(
                'title').text.strip().replace(' of 5 bubbles', '')

        title_element = review.find(
            'div', attrs={'data-test-target': 'review-title'})
        if title_element:
            review_data['title'] = title_element.text.strip()

        text_element = review.find(
            'div', attrs={'data-test-target': 'review-body'})
        if text_element:
            review_data['text'] = text_element.text.strip()

        date_element = review.find('div', class_='neAPm')
        if date_element:
            child_divs = date_element.find_all('div')
            if child_divs:
                review_data['date'] = child_divs[0].text.strip().replace(
                    'Written ', '')

        reviews.append(review_data)
        time.sleep(3)

    return reviews


def save_to_csv(restaurant_info, reviews, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header
        header = ['RESTAURANT_NAME', 'PRICE_LEVEL', 'CUISINE_TYPE', 'TOTAL_RATING',
                  'TOTAL_REVIEWS', 'FOOD_RATING', 'SERVICE_RATING', 'VALUE_RATING',
                  'ATMOSPHERE_RATING', 'RANKING', 'CITY', 'ADDRESS', 'PHONE_NO',
                  'RATING', 'REVIEW_TITLE', 'REVIEW_DETAILS', 'REVIEW_DATE']
        writer.writerow(header)

        # Write reviews with restaurant info
        for review in reviews:
            row = [
                restaurant_info['name'],
                restaurant_info['price_level'],
                restaurant_info['cuisine_type'],
                restaurant_info['total_rating'],
                restaurant_info['total_reviews'],
                restaurant_info['food_rating'],
                restaurant_info['service_rating'],
                restaurant_info['value_rating'],
                restaurant_info['atmosphere_rating'],
                restaurant_info['ranking'],
                restaurant_info['city'],
                restaurant_info['address'],
                restaurant_info['phone_no'],
                review['rating'],
                review['title'],
                review['text'],
                review['date']
            ]
            writer.writerow(row)


def main():
    url = 'https://www.tripadvisor.com/Restaurant_Review-g60763-d478965-Reviews-or45-Gallaghers_Steakhouse-New_York_City_New_York.html'
    headers, proxies = setup_request()

    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(10)

        restaurant_info = get_restaurant_info(soup)
        reviews = scrape_reviews(soup)

        save_to_csv(restaurant_info, reviews,
                    'tripadvisor_ny_restaurant_reviews_details_page_1.csv')
        print("All information saved successfully")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during requests to {url} : {str(e)}")


if __name__ == "__main__":
    main()
