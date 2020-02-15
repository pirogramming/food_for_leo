import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from crawling.brand_crawling import *
from core.models import *


def crawling_mall3():
    brands = Brand.objects.all().order_by('name')  # 함수분리시 view에서 처리/매개변수로 받기
    brand_url_base = 'http://www.dogpre.com/shop/goods/goods_list.php?category=036&search_word=&parent_sno=&scroll=0&cateType=&v_category=&category=036&search_brand%5B%5D='
    start = 0
    index = 0
    for brand in brands:
        for i in range(start, len(brand_list[3])):
            if index >= len(brand_list[3]):
                break
            elif str(brand) == brand_list[3][i]:
                Mall.objects.update_or_create(
                    name='president',
                    brand=brand,
                    logo='http://www.apslove.com/shop/data/skin/aps2016/img/banner/main_header_logo.gif',
                    brand_url=brand_url_base + pre_brand_selector[index].get('value'),
                )
                index += 1
                start = i
                break
            elif str(brand) < brand_list[3][i]:
                start = i
                break


# mall의 브랜드url을 찾아들어가서 상품 상세정보 들어가는 url크롤링 해온다.
# product 객체 만든다.
def crawling_mall3_product():
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
            soup = bs(html, 'lxml')
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
                sto = 10
            elif sto == '재고없음':
                sto = 0
            else:
                sto = sto.split('개')[0].split(' ')[-1].strip()
            # 디테일 사진 : 있으면 넣고 없으면 null
            if len(soup.select('#goods_desc_img')) > 0:
                d_image = soup.select('#goods_desc_img')[0].get('src')
            else:
                d_image = None
            Product.objects.update_or_create(product_url='http://www.dogpre.com' + product.get('href'),
                                             mall=br_m,
                                             name=soup.select('fieldset > div.hd  h2')[0].text,
                                             price=pri,
                                             stock=sto,
                                             img_main=soup.select('#detail_image')[0].get('src'),
                                             img_detail=d_image,
                                             made_in=soup.select('div.section.new-write > ul > li:nth-child(2) > p')[
                                                 0].text,
                                             )


if __name__ == '__main__':
    brand_crawling()
    brand_create_first()
    brand_create()
    crawling_mall3()
    crawling_mall3_product()
