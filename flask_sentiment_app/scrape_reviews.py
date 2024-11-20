from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from time import sleep

# Function to scrape Amazon reviews with improved logic
def scrape_amazon_reviews(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    reviews = []
    page = 1

    while len(reviews) < 400:
        try:
            paginated_url = f"{product_url}/ref=cm_cr_arp_d_paging_btm_next_{page}?pageNumber={page}"
            response = requests.get(paginated_url, headers=headers)

            if response.status_code != 200:
                print(f"Failed to retrieve page {page} of Amazon reviews.")
                break

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract reviews from the current page
            review_elements = soup.find_all('span', {'data-hook': 'review-body'})
            if not review_elements:
                print(f"No reviews found on page {page}.")
                break

            for review_element in review_elements:
                reviews.append(review_element.get_text(strip=True))
                if len(reviews) >= 400:  # Stop if we reach the limit
                    break

            # Check if there are more pages
            next_page = soup.find('li', {'class': 'a-last'})
            if not next_page or not next_page.find('a'):
                break  # Exit if there are no more pages

            page += 1
            sleep(1)  # Respectful delay
        except Exception as e:
            print(f"Error while scraping Amazon: {e}")
            break

    return reviews

# Function to scrape Flipkart reviews with Selenium
def scrape_flipkart_reviews(product_url):
    # Specify the path to the Chromium binary
    options = Options()
    options.binary_location = "/opt/homebrew/bin/chromium"  # Update with the correct path to Chromium
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use WebDriverManager to handle the ChromeDriver setup
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    reviews = []
    try:
        driver.get(product_url)

        # Wait for the reviews to load
        wait = WebDriverWait(driver, 10)
        while len(reviews) < 400:
            # Locate review containers
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_1AtVbE")))
            review_elements = driver.find_elements(By.CLASS_NAME, "t-ZTKy")

            # Append reviews to the list
            for element in review_elements:
                reviews.append(element.text.strip())
                if len(reviews) >= 400:
                    break

            # Navigate to the next page
            try:
                next_button = driver.find_element(By.CLASS_NAME, "_1LKTO3")
                if 'disabled' in next_button.get_attribute("class"):
                    break
                next_button.click()
                sleep(2)  # Short delay for content to load
            except Exception:
                break  # Exit if the next button is missing or disabled

    except Exception as e:
        print(f"Error while scraping Flipkart: {e}")
    finally:
        driver.quit()

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
