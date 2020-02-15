import os
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import django

django.setup()
from crawling.brand_crawling import *
from core.models import *
import time


def parse_brand():
    req = requests.get('http://queenpuppy.co.kr/shop/cate_main.html?category=182')
    req.encoding = 'euc-kr'
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    brand = soup.select('.cate a')
    data = {}
    brand_list_compare = []
    for i in brand:
        data[i.text.split(' ')[0]] = i.get('href')
        brand_list_compare.append([i.text.split(' ')[0]])
    for x, y in data.items():
        Mall.objects.update_or_create(name="QueenNPuppy", brand_id=Brand.objects.filter(name=x).first().id,
                                      brand_url="http://queenpuppy.co.kr" + y,
                                      logo='http://queenpuppy.co.kr/img/QP_LOGO.png')
        req = requests.get("http://queenpuppy.co.kr" + y)
        req.encoding = 'euc-kr'
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        url = soup.select(
            '.product .picture a '
        )
        for product_url in url:
            req = requests.get("http://queenpuppy.co.kr" + product_url.get('href'))
            req.encoding = 'euc-kr'
            html = req.text
            soup = BeautifulSoup(html, 'lxml')
            price = soup.select(
                'div.content.price '
            )
            price_revised_1 = price[0].text.strip()[:-1].split(",")
            price_revised_2 = ''.join(price_revised_1)

            name = soup.select('.d_part_1 div.name ')[0].text.strip()

            while (name[0] == '['):
                name = name.split(']', 1)[1].strip()

            if '[' in name:
                name = name.split('[')[0].strip('\t').strip()

            if '?' in name:
                name = name.split('?')[0].strip()

            if '(' in name:
                name = name.split('(')[0].strip()
            else:
                name = name.strip()

            name = name.replace(' 세트', '')

            made_in = soup.select(
                '.info_line > .content '
            )
            img_main = soup.select(
                'div.photo_L > img'
            )
            stock = soup.select(
                '.soldout > div.ment'
            )
            if stock:
                stock_revised = 0
            else:
                stock_revised = 10
            # print(img_main)
            img_detail = soup.select(
                '#pd_detail0 > div.image img'
            )

            if img_detail:
                img_detail_revised = img_detail[0].get('src')
            else:
                img_detail_revised = ""

            # print(img_detail)

            # "이름", "브랜드", "가격", "재고", "detail_url", "img_main", "원산지"]
            Product.objects.update_or_create(name=name,
                                             made_in=made_in[0].text,
                                             price=int(price_revised_2),
                                             stock=stock_revised,
                                             product_url="http://queenpuppy.co.kr" + product_url.get('href'),
                                             mall_id=Mall.objects.filter(
                                                 brand_id=Brand.objects.filter(name=x).first().id).first().id,
                                             img_main=img_main[0].get('src'),
                                             img_detail=img_detail_revised,

                                             )


if __name__ == '__main__':
    start_time = time.time()
    # 4개의 프로세스를 사용합니다.
    # get_contetn 함수를 넣어줍시다.
    brand_crawling()
    brand_create()
    brand_create_first()
    parse_brand()
