import time

import requests
from requests.exceptions import (ConnectTimeout, ConnectionError, ReadTimeout)

from .resources_v2 import CJProduct


class APIError(Exception):
    pass


class Client:
    base_url = "https://developers.cjdropshipping.com/"
    Products = CJProduct
    max_page_size = 200  # according to docs
    default_page_size = 20
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
                resp = requests.get(url, params=payload, headers=headers)
                if resp.status_code >= 500:
                    time.slee(5)
                    continue

                try:
                    data = resp.json()
                    if 'code' in data and data['code']:
                        code = data['code']
                        if code == 1600000:
                            time.sleep(7)
                        elif code in [1600200, 1600201]:
                            time.sleep(1)
                        else:
                            break
                    else:
                        time.sleep(3)
                except:
                    time.sleep(1)
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
        :url https://developers.cjdropshipping.com/api2.0/v1/product/getCategory
        :param page_num: For legacy compitable only
        :param page_size: For legacy compitable only
        :return:
        """

        return self.json_request(self.Products.get_categories)

    def view_products(self, page_num = 1, page_size = 20, category_id = None):
        """
        :url https://developers.cjdropshipping.com/api2.0/v1/product/list
        :param page_num: the current page to show
        :param page_size: number to show per page (default 20, maximum is 200)
        :param category_id: category id (maximum length 200)
        :return:
        """
        if page_size and page_size > 0:
            if page_size > self.max_page_size:
                page_size  = self.max_page_size
        else:
            page_size = self.default_page_size
        return self.json_request(self.Products.view_category, payload={
            'pageNum': page_num or self.default_page_number,
            'pageSize': page_size,
            'categoryId': category_id
        })

    def product_details(self, product_id):
        """
        :url https://developers.cjdropshipping.com/api2.0/v1/product/query
        :param product_id: Product id
        :return:
        """
        return self.json_request(self.Products.view_product, payload={
            'pid': product_id
        })

    def product_ships_from(self, variant_id):
        """
        :url https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryByVid?vid=7874B45D-E971-4DC8-8F59-40530B0F6B77
        :param variant_id: Variant id
        :return:
        """
        return self.json_request(self.Products.product_ships_from, payload={
            'vid': variant_id
        })
