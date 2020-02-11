import requests
from bs4 import BeautifulSoup as bs
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from core.models import *


def crawling_brand():
    req = requests.get('http://www.dogpre.com/shop/goods/goods_list.php?category=036')
    req.encoding = 'euc-kr'
    html = req.text
    soup = bs(html, 'html.parser')
    # 브랜드 이름을 가져오는 리스트
    global bl
    bl = [b.text.strip().split('(')[0] for b in soup.select('.nano-content.nano-content-scroll label')]
    # 브랜드 이름의 value를 가져오는 리스트
    global brand_list4
    brand_list4 = soup.select('.nano-content.nano-content-scroll label input')
    # 브랜드 객체 생성
    for brand in bl:
        Brand.objects.create(name=brand)


def crawling_mall():
    brand_url_base = 'http://www.dogpre.com/shop/goods/goods_list.php?category=036&search_word=&parent_sno=&scroll=0&cateType=&v_category=&category=036&search_brand%5B%5D='
    brand_name_indx = 0
    for br in brand_list4:
        m = Mall.objects.create(name='president',
                                brand_url=brand_url_base + br.get('value'),
                                brand=Brand.objects.filter(name=bl[brand_name_indx]).first(),
                                logo='http://www.dogpre.com/?ref=nav_logo')
        brand_name_indx += 1


# mall의 브랜드url을 찾아들어가서 상품 상세정보 들어가는 url크롤링 해온다.
# product 객체 만든다.
def crawling_product():
    for br_m in Mall.objects.all():
        req = requests.get(br_m.brand_url)
        req.encoding = 'euc-kr'
        html = req.text
        soup = bs(html, 'html.parser')
        # 제품 url
        product_url_list = soup.select(
            'div.srch-cont > div.srch-prdc-list.row.del-tag.cate_list.listStyleOther div > a:nth-child(2)')
        for product in product_url_list:
            url = 'http://www.dogpre.com' + product.get('href')
            req = requests.get(url)
            req.encoding = 'euc-kr'
            html = req.text
            soup = bs(html, 'html.parser')
            # 가격
            # div.price_info > table > tbody > tr:nth-child(1) > td > span
            is_discount = \
                soup.select(
                    'div.cont > div.price_info > table > tbody  tr.price.discount > td > span.discount-price.red')[
                    0].text.strip().split('원')[0].replace(',', '')
            if is_discount == '0':
                pri = soup.select('div.cont > div.price_info > table > tbody  tr  td.price_view > span')[
                    0].text.strip().split('원')[0].replace(',', '')
            else:
                pri = soup.select(
                    'div.cont > div.price_info > table > tbody  tr.price.discount > td > span.discount-price.red')[
                    0].text.strip().split('원')[0].replace(',', '')
            # 재고
            sto = soup.select('div.cont > div.stock  dl  dt')[0].text.strip()
            if sto == '재고있음':
                sto = 10000
            elif sto == '재고없음':
                sto = 0
            else:
                sto = sto.split('개')[0].split(' ')[-1].strip()
            # 디테일 사진 : 있으면 넣고 없으면 null
            if len(soup.select('#goods_desc_img')) > 0:
                d_image = soup.select('#goods_desc_img')[0].get('src')
            else:
                d_image = None
            Product.objects.create(product_url=product.get('href'),
                                   mall=br_m,
                                   name=soup.select('fieldset > div.hd  h2')[0].text,
                                   price=pri,
                                   stock=sto,
                                   img_main=soup.select('#detail_image')[0].get('src'),
                                   img_detail=d_image,
                                   made_in=soup.select('div.section.new-write > ul > li:nth-child(2) > p')[0].text,
                                   )


if __name__ == '__main__':
    crawling_brand()
    crawling_mall()
    crawling_product()