import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import csv
from datetime import datetime
import os

class AbstractScraper:
    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('ScraperLogger')
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def scrape(self):
        pass


class NotinoScraper(AbstractScraper):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def scrape(self):
        options = Options()
        options.headless = True
        options.add_argument("--private")  # Adding private browsing mode
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

        try:
            self.logger.info(f"Opening URL: {self.url}")
            driver.get(self.url)
            sleep(5)  # Wait for the page to fully load, adjust as needed

            # Click on "I agree" button
            try:
                agree_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/a[2]/span")
                agree_button.click()
                sleep(2)
            except NoSuchElementException:
                self.logger.warning("Agree button not found, proceeding without clicking.")

            # Scroll down
            self.logger.info("Scrolling down the page")
            driver.execute_script("window.scrollBy(0, 600);")
            sleep(2)

            # Click on "Brand"
            brand_selector = "div.styled__CollapsibleWrapper-sc-1gtgo38-0:nth-child(3) > div:nth-child(1) > svg:nth-child(1)"
            brand = driver.find_element(By.CSS_SELECTOR, brand_selector)
            brand.click()
            sleep(3)

            # Click on "Apis Natural Optima"
            Apis_selector = "div.styled__FilterGroupItemsWrapper-sc-81vbf9-1:nth-child(2) > a:nth-child(1) > span:nth-child(1)"
            Apis = driver.find_element(By.CSS_SELECTOR, Apis_selector)
            Apis.click()
            sleep(3)

            # Click on "Product"
            product_selector = ".sc-iKOmoZ"
            product = driver.find_element(By.CSS_SELECTOR, product_selector)
            product.click()
            sleep(3)

            # Scroll down
            self.logger.info("Scrolling down the page")
            driver.execute_script("window.scrollBy(0, 300);")
            sleep(2)

            # Click on "Ingredients"
            ingredients_selector = "#tabComposition"
            ingredients = driver.find_element(By.CSS_SELECTOR, ingredients_selector)
            ingredients.click()
            sleep(3)

            # Click on "Image"
            image_selector = "#pd-image-main"
            image = driver.find_element(By.CSS_SELECTOR, image_selector)
            image.click()
            sleep(3)

            # Handle CAPTCHA if present
            try:
                captcha_button = driver.find_element(By.ID, "checkbox")
                captcha_button.click()
                sleep(10)
            except NoSuchElementException:
                self.logger.info("No CAPTCHA found, continuing...")

            product_name = "Apis Natural Optima"
            brand_name = "APIS"
            price = "3.90"
            product_url = "https://www.notino.co.uk/apis-natural-cosmetics/optima-toothpaste-with-dead-sea-minerals/"
            image_url = "Your image URL"

            # Define the directory where you want to save the CSV file
            save_directory = r'C:\Users\marti\PycharmProjects\forloop'

            # Check if the directory exists, if not, create it
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            # Save the scraped data to CSV in the specified directory
            csv_file_path = os.path.join(save_directory, 'notino_raw.csv')
            with open(csv_file_path, 'w', newline='') as csvfile:
                fieldnames = ['product_name', 'brand', 'price', 'url', 'image']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    'product_name': product_name,
                    'brand': brand_name,
                    'price': price,
                    'url': product_url,
                    'image': image_url
                })
            self.logger.info(f"Data saved to {csv_file_path}")

        except TimeoutException:
            self.logger.warning("TimeoutException: Brand window didn't become clickable. Pausing execution.")
            input("Please solve the CAPTCHA and press Enter to resume...")
            self.scrape()  # Resume scraping after CAPTCHA solved

        finally:
            driver.quit()


if __name__ == "__main__":
    scraper = NotinoScraper('https://www.notino.co.uk/toothpaste/')
    scraper.scrape()
