import requests
from bs4 import BeautifulSoup

# Function to scrape Amazon reviews with pagination
def scrape_amazon_reviews(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    reviews = []
    page = 1

    while len(reviews) < 400:
        # Modify the URL to include the pagination parameter
        paginated_url = f"{product_url}/ref=cm_cr_arp_d_paging_btm_next_{page}?pageNumber={page}"
        response = requests.get(paginated_url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page} of Amazon reviews.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract reviews from the current page
        review_elements = soup.find_all('span', {'data-hook': 'review-body'})
        for review_element in review_elements:
            reviews.append(review_element.get_text(strip=True))
            if len(reviews) >= 400:  # Stop if we reach the limit
                break

        # Check if there are more pages
        next_page = soup.find('li', {'class': 'a-last'})
        if not next_page or not next_page.find('a'):
            break  # Exit if there are no more pages

        page += 1

    return reviews

# Function to scrape Flipkart reviews with pagination
def scrape_flipkart_reviews(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    reviews = []
    page = 1

    while len(reviews) < 400:
        # Modify the URL to include the pagination parameter
        paginated_url = f"{product_url}&page={page}"
        response = requests.get(paginated_url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve page {page} of Flipkart reviews.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract reviews from the current page
        review_elements = soup.find_all('div', {'class': 't-ZTKy'})
        for review_element in review_elements:
            reviews.append(review_element.get_text(strip=True))
            if len(reviews) >= 400:  # Stop if we reach the limit
                break

        # Check if there are more pages
        next_button = soup.find('a', {'class': '_1LKTO3'})
        if not next_button or 'disabled' in next_button.get('class', []):
            break  # Exit if there are no more pages

        page += 1

    return reviews

# General function to decide which platform to scrape from
def scrape_reviews(product_url):
    if "amazon" in product_url:
        print("Scraping Amazon reviews...")
        return scrape_amazon_reviews(product_url)
    elif "flipkart" in product_url:
        print("Scraping Flipkart reviews...")
        return scrape_flipkart_reviews(product_url)
    else:
        print("Unsupported URL. Please provide an Amazon or Flipkart product link.")
        return []
