import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from crawling.brand_crawling import *
from core.models import *

def mall2_crawling_mall():
    brands = Brand.objects.all().order_by('name')
    req = requests.get('http://www.dogskingdom.co.kr/shop/goods/goods_list.php?&category=001')
    html = req.text
    soup = bs(html, 'html.parser')
    bl = soup.select(".list_subcate a")
    brand_3_url = {}  # brandName-url 정렬 위한 딕셔너리
    for i in bl:
        brand_3_url[i.getText()] = i.get('href')
    brand_3_url = sorted(brand_3_url.items())  # 딕셔너리 내 원소의 키, 값 튜플로 반환
    start = 0
    indx = 0


    for brand in brands:
        for i in range(start, len(brand_3_url)):

            if indx >= len(brand_3_url):
                break
            elif str(brand) == brand_3_url[i][0]:
                Mall.objects.update_or_create(
                    name='kingdom',
                    brand=brand,
                    logo='http://www.dogskingdom.co.kr/shop/data/skin/apple_tree/img/banner/54564.jpg',
                    brand_url=f"http://www.dogskingdom.co.kr/shop/goods/goods_list.php{brand_3_url[indx][1]}",
                )
                indx += 1
                start = i
                break
            elif str(brand) < brand_3_url[i][0]:
                start = i
                break


def mall2_crawling_product():
    for mall in Mall.objects.all():
        req = requests.get(mall.brand_url)
        html = req.text
        soup = bs(html, 'html.parser')
        product_list = soup.select(".space")
        for product in product_list:
            product_url = f"http://www.dogskingdom.co.kr/shop/{product.find('a').get('href')}"

            req = requests.get(product_url)
            html = req.text
            soup = bs(html, 'html.parser')

            product_info = soup.select(".thume_wrap.border_box")
            for info in product_info:
                img_main = f"http://www.dogskingdom.co.kr/shop/data/{info.find('img').get('src')}"

            img_detail = soup.select("#contents")
            for img in img_detail:
                img_detail = f"http://www.dogskingdom.co.kr/{img.get('src')}"

            stocks = [i.text.strip() for i in soup.select('.sub.tbl_opt td')]
            if '품절된 상품입니다' == stocks:
                stock = 0
            else:
                stock = 10000

            name = soup.select(".goods_name")[0].text
            if ']' in name:
                name = name.split(']')[1].strip()
            else:
                name = name

            Product.objects.update_or_create(
                name=name,
                mall=mall,
                price=[i.text for i in soup.select("#price")][0].replace(',', ''),
                stock=stock,
                product_url=product_url,
                img_main=img_main,
                img_detail=img_detail,
                made_in=[i.text for i in soup.select('.price tr:nth-of-type(3) td')][0],
            )


if __name__ == '__main__':
    brand_crawling()
    brand_create_first()
    brand_create()
    mall2_crawling_mall()
    mall2_crawling_product()
