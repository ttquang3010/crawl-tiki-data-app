import datetime
import logging

import requests
from app import app
from app.const.CONST import FETCH_TIKI_API_LIMIT
from flask import session

from .api_fetcher import APIFetcher

logger = logging.getLogger()

class FetcherByCategory(APIFetcher):
    def __init__(self, params):
        super().__init__(params)
    
    def fetch_by_category(self):
        url = 'https://tiki.vn/api/personalish/v1/blocks/listings'
        product_list = []
        
        # `last_page`: the number of pages to fetch
        # `last_page_limit`: the limit of products to fetch on the last page
        last_page = self.params['page']
        last_page_limit = self.params['limit']
       
        # Loop through the pages of the API response and fetches the data for each page
        for page in range(1, last_page + 1):

            # Set the `page` and `limit` parameters in the API request based on the current page and the last page
            self.params['page'] = page
            if page != last_page:
                self.params['limit'] = FETCH_TIKI_API_LIMIT
            else:
                self.params['limit'] = last_page_limit
            
            # Fetch the data from the API using the `fetch` method from the `APIFetcher` class
            try: 
                # Check if the user's session has timed out or not before making a request to the Tiki API
                now = datetime.datetime.now()
                last_active = session['last_active']
                delta = now - last_active
                if delta.seconds > app.permanent_session_lifetime.seconds:
                    session['last_active'] = now
                    logger.exception("Session time out")
                    return
                
                response = self.fetch(url, self.params)
                response.raise_for_status()
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                logger.exception("Error occurred while fetching data for page %s: %s", page, e)
                continue
            except Exception as e:
                logger.exception("Something went wrong while fetching data for page %s: %s", page, e)
                continue

            # Parse the JSON response from the Tiki API endpoint and extract the 'data' field from it
            try:
                data = response.json().get('data')
            except ValueError as e:
                logger.exception("Error parsing response JSON at page %s: %s", page, e)
                continue

            # Loop through the records in the data and creates a dictionary of product information for each record
            for record in data:
                product_item = {
                    'id': record.get('id'),
                    'sku': record.get('sku'),
                    'name': record.get('name'),
                    'url_key': record.get('url_key'),
                    'url_path': record.get('url_path'),
                    'type': record.get('type'),
                    'author_name': record.get('author_name'),
                    'book_cover': record.get('book_cover'),
                    'brand_name': record.get('brand_name'),
                    'short_description': record.get('short_description'),
                    'price': record.get('price'),
                    'list_price': record.get('list_price'),
                    'badges': record.get('badges'),
                    'badges_new': record.get('badges_new'),
                    'discount': record.get('discount'),
                    'discount_rate': record.get('discount_rate'),
                    'rating_average': record.get('rating_average'),
                    'review_count': record.get('review_count'),
                    'order_count': record.get('order_count'),
                    'favourite_count': record.get('favourite_count'),
                    'thumbnail_url': record.get('thumbnail_url'),
                    'thumbnail_width': record.get('thumbnail_width'),
                    'thumbnail_height': record.get('thumbnail_height'),
                    'freegift_items': record.get('freegift_items'),
                    'has_ebook': record.get('has_ebook'),
                    'inventory_status': record.get('inventory_status'),
                    'is_visible': record.get('is_visible'),
                    'productset_id': record.get('productset_id'),
                    'productset_group_name': record.get('productset_group_name'),
                    'seller': record.get('seller'),
                    'is_flower': record.get('is_flower'),
                    'is_gift_card': record.get('is_gift_card'),
                    'inventory': record.get('inventory'),
                    'url_attendant_input_form': record.get('url_attendant_input_form'),
                    'option_color': record.get('option_color'),
                    'stock_item': record.get('stock_item'),
                    'salable_type': record.get('salable_type'),
                    'seller_product_id': record.get('seller_product_id'),
                    'installment_info': record.get('installment_info'),
                    'url_review': record.get('url_review'),
                    'bundle_deal': record.get('bundle_deal'),
                    'quantity_sold': record.get('quantity_sold'),
                    'video_url': record.get('video_url'),
                    'tiki_live': record.get('tiki_live'),
                    'original_price': record.get('original_price'),
                    'shippable': record.get('shippable'),
                }
                # Append this dictionary to the `product_list` list
                product_list.append(product_item)
        return product_list