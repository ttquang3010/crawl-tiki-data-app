import logging

import requests

from .api_fetcher import APIFetcher

logger = logging.getLogger()

class FetcherCategoryList(APIFetcher):
    def __init__(self):
        super().__init__()
    
    def fetch_category_list(self):
        url = 'https://tiki.vn/api/personalish/v1/blocks/categories?block_code=categories_for_you&page_size=100'
        category_list = []
       
        # Fetch a category list from Tiki API endpoint
        try:
            # Call `fetch()` method from the `APIFetcher` class to make a request to the API
            response = self.fetch(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.exception("Error fetching product list by category: %s", e)
            return category_list
        
        # Parse the JSON response from the Tiki API endpoint and extract the 'items' field from it
        try:
            data = response.json().get('items')
        except ValueError as e:
            logger.exception("Error parsing response JSON: %s", e)
            return category_list

        # For each category in the list, create a dictionary `category_item` that contains various attributes of the category
        for record in data:
            category_item = {
                'id': record.get('id'),
                'parent_id': record.get('parent_id'),
                'name': record.get('name'),
                'url': record.get('url'),
            }
            # Append this dictionary to the `category_list` list
            category_list.append(category_item)
        return category_list
    