import logging
import requests
from requests.exceptions import RequestException

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

    def get_request(self, url, headers=None, params=None):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            self.logger.info(f"GET request to {url} successful")
            return response
        except RequestException as e:
            self.logger.error(f"GET request to {url} failed: {e}")
            return None

    def post_request(self, url, headers=None, data=None, json=None):
        try:
            response = requests.post(url, headers=headers, data=data, json=json)
            response.raise_for_status()
            self.logger.info(f"POST request to {url} successful")
            return response
        except RequestException as e:
            self.logger.error(f"POST request to {url} failed: {e}")
            return None

    def scrape(self):
        pass
