import logging

import requests

from ..fetcher import Fetcher

logger = logging.getLogger()

class APIFetcher(Fetcher):
    def __init__(self, params=None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
        self.params = params

    def fetch(self, url, params=None):
    
        # Fetch data from a given URL using HTTP GET request and handle exceptions that may occur
        try:
            response = requests.get(f'{url}', headers=self.headers, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.exception("HTTP Error: %s", e)
            return None
        except requests.exceptions.ConnectionError as e:
            logger.exception("Error Connecting: %s", e)
            return None
        except requests.exceptions.Timeout as e:
            logger.exception("Timeout Error: %s", e)
            return None
        except requests.exceptions.RequestException as e:
            logger.exception("Something went wrong: %s", e)
            return None