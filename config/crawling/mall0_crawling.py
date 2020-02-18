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


def mall0_crawling():
    brands = Brand.objects.all().order_by('name')  # 함수분리시 view에서 처리/매개변수로 받기

    html_text = requests.get('http://www.apslove.com/shop/goods/goods_list.php?category=006001').text
    soup = bs(html_text, 'html.parser')
    brand_1_url = {}  # brandName-url 정렬 위한 딕셔너리
    for i in soup.select('.category-sub-new tr:nth-of-type(1) ul a'):
        brand_1_url[i.getText()] = i.get('href')
    brand_1_url = sorted(brand_1_url.items())  # 딕셔너리 내 원소의 키, 값 튜플로 반환

    start = 0
    index = 0

    for brand in brands:
        for i in range(start, len(brand_1_url)):
            if index >= len(brand_1_url):
                break
            elif str(brand) == brand_1_url[i][0]:  # brandName은 튜플의 0번 인덱스
                Mall.objects.update_or_create(
                    name='동물사랑APS',
                    brand=brand,
                    logo='http://www.apslove.com/shop/data/skin/aps2016/img/banner/main_header_logo.gif',
                    brand_url=f'http://www.apslove.com/shop/goods/goods_list.php{brand_1_url[index][1]}',
                    # url은 튜플의 1번 인덱스
                )
                index += 1
                start = i
                break
            elif str(brand) < brand_1_url[i][0]:
                start = i
                break


def mall0_product_crawling():
    malls = Mall.objects.all().order_by('brand__name')  # view함수에서

    for mall in malls:
        html_text = requests.get(mall.brand_url)
        soup = bs(html_text.text, 'html.parser')
        products = [i for i in soup.select('#load-ajax div.goodsnm > a')]
        for product in products:
            product_pass_url = product.get('href').split('../')[1]
            if (product_pass_url == 'goods/goods_view.php?goodsno=20835&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=21067&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=19574&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=19574&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=19571&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9189&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=19370&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=19371&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9181&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9194&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9176&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=16842&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=16841&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9186&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9182&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9179&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9177&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9188&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9185&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9192&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9195&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=13106&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9180&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9178&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=19573&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=18774&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=9183&category=006001012027') or (
                    product_pass_url == 'goods/goods_view.php?goodsno=9193&category=006001012027') or \
                    (product_pass_url == 'goods/goods_view.php?goodsno=21281&category=006001012001') or (
                    '006001012046' in product_pass_url):  # '퓨어럭스'제외
                continue

            html_text = requests.get(f'http://www.apslove.com/shop/{product.get("href").split("..")[1]}').text
            print(f'http://www.apslove.com/shop/{product.get("href").split("..")[1]}')  #
            soup = bs(html_text, 'html.parser')
            get_stock = get_apslove_stock(soup)
            if get_stock == 777:
                continue
            Product.objects.update_or_create(
                name=get_apslove_name(soup),
                mall=mall,
                price=soup.select('#price')[0].text.split('원')[0].replace(',', ''),
                stock=get_stock,
                product_url=f'http://www.apslove.com/shop/goods{product.get("href").split("../goods")[1]}',
                img_main=f'http://www.apslove.com/shop{soup.select("#objImg")[0].get("src").split("..")[1]}',
                img_detail=get_apslove_imgDetail(soup),
                made_in=get_apslove_made_in(soup)
            )


def get_apslove_name(soup):
    name = soup.select("#goods_spec > form > div.goodsnm.dote-bottom > b")[0].text.strip()

    while ('[' in name[0]):
        name = name.split(']', 1)[1].strip()
    if '/' or '-' in name:
        name = name.split('-')[0].strip()
        name = name.split('/')[0].strip()
    else:
        name = name
    name = name.replace('(set)', '')
    name = name.replace('세트', '')
    name = name.replace('(강아지)', '')
    name = name.replace('강아지사료', '')
    print(name)
    return name


def get_apslove_stock(soup):
    stock = soup.select('#goods_spec > form table:nth-child(6)')
    stock_1 = soup.select('#goods_spec > form table:nth-child(7)')
    stock_2 = soup.select('#goods_spec > form table:nth-child(8)')

    # 제외 product
    if soup.select('#goods_spec form > table:nth-of-type(3) tr:nth-of-type(2) > td > div > select') != []:
        return 777

    # case 분류
    if stock:
        if '구매수량' in stock[0].text:
            if "품절된" in stock[0].text:
                return 0
            else:
                return 10
    if stock_1:
        if '구매수량' in stock_1[0].text:
            if "품절된" in stock_1[0].text:
                return 0
            else:
                return 10
    if stock_2:
        if '구매수량' in stock_2[0].text:
            if "품절된" in stock_2[0].text:
                return 0
            else:
                return 10


def get_apslove_imgDetail(soup):
    if soup.select('#view_contents > p img') == []:
        if 'http:' in soup.select('#view_contents > img')[0].get('src'):
            imgUrl = soup.select('#view_contents > img')[0].get('src')
        else:
            imgUrl = f'http://www.apslove.com{soup.select("#view_contents > img")[0].get("src")}'
    else:
        if 'http:' in soup.select("#view_contents > p img")[0].get("src"):
            imgUrl = soup.select("#view_contents > p img")[0].get("src")
        else:
            imgUrl = f'http://www.apslove.com{soup.select("#view_contents > p img")[0].get("src")}'

    return imgUrl


def get_apslove_made_in(soup):
    madeIn = soup.select('#goods_spec > form table:nth-child(6)')
    madeIn_1 = soup.select('#goods_spec > form table:nth-child(7)')
    madeIn_2 = soup.select('#goods_spec > form table:nth-child(8)')

    if madeIn:
        if "원산지" in madeIn[0].text:
            return (madeIn[0].text.split('\n')[3].split('원산지')[1])
    if madeIn_1:
        if "원산지" in madeIn_1[0].text:
            return (madeIn_1[0].text.split('\n')[3].split('원산지')[1])
    if madeIn_2:
        if "원산지" in madeIn_2[0].text:
            return (madeIn_2[0].text.split('\n')[3].split('원산지')[1])


if __name__ == '__main__':
    brand_crawling()
    brand_create_first()
    brand_create()
    mall0_crawling()
    mall0_product_crawling()
