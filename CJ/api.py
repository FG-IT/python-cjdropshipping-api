import time

import requests
from requests.exceptions import (ConnectTimeout, ConnectionError, ReadTimeout)

from .resources import CJProduct


class APIError(Exception):
    pass


class Client:
    base_url = "https://developers.cjdropshipping.com/"
    test_url = "api/account/start"
    Products = CJProduct
    max_page_size = 50  # according to docs
    default_page_size = 10
    default_page_number = 1

    def __init__(self, secret_key=None, max_retries=7):
        self.secret_key = secret_key 
        self.max_retries = max_retries

    def build_url(self, resource):
        return f"{self.base_url}{resource}"

    def json_request(self, resource, payload=None):
        if not payload:
            payload = {}
        url = self.build_url(resource)
        headers = {'CJ-Access-Token': self.secret_key}

        retries = self.max_retries
        while retries > 0:
            try:
                resp = requests.post(url, json=payload, headers=headers)
                break
            except (ConnectTimeout, ReadTimeout) as e:
                retries -= 1
                if retries <= 0:
                    raise
                else:
                    time.sleep(1)
            except ConnectionError as e:
                retries -= 1
                if retries <= 0:
                    raise

        if resp.status_code == 200:
            return resp.json()
        else:
            raise APIError(f"POST {resource} {resp.status_code}")

    def get_product_categories(self, page_num=None, page_size=None):
        """
        :url https://developers.cjdropshipping.com/cj/cj-products.html#view-category
        :param page_num: the current page to show
        :param page_size: number to show per page (max 50)
        :return:
        """

        return self.json_request(self.Products.get_categories, payload={
            'pageNum': page_num or self.default_page_number,
            'pageSize': page_size or self.default_page_size
        })

    def view_category(self, page_num, page_size):
        return self.json_request(self.Products.view_category, payload={
            'pageNum': page_num or self.default_page_number,
            'pageSize': page_size or self.default_page_size
        })

    def view_products(self, page_num, page_size, category_id):
        return self.json_request(self.Products.view_category, payload={
            'pageNum': page_num or self.default_page_number,
            'pageSize': page_size or self.default_page_size,
            'categoryId': category_id
        })

    def product_details(self, product_id):
        return self.json_request(self.Products.view_product, payload={
            'pid': product_id
        })

    def product_ships_from(self, product_id, variant_id, do_variant=True):
        """
        It's either 'pid' or 'vid' (variant id) not sure
        :param product_id:
        :param variant_id:
        :return:
        """
        if do_variant:
            return self.json_request(self.Products.product_ships_from, payload={
                'vid': variant_id
            })
        else:
            return self.json_request(self.Products.product_ships_from, payload={
                'pid': product_id
            })
