import os
from bs4 import BeautifulSoup


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import django
django.setup()
from crawling.brand_crawling import *
from crawling.mall0_crawling import *
from crawling.mall1_crawling import *
from crawling.mall2_crawling import *
from crawling.mall3_crawling import *

from core.models import *
import time


if __name__ == '__main__':
    brand_crawling()
    brand_create_first()
    brand_create()
    mall0_crawling()
    mall0_product_crawling()
    parse_brand()
    mall2_crawling_mall()
    mall2_crawling_product()
    crawling_mall3()
    crawling_mall3_product()