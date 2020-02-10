import requests
from bs4 import BeautifulSoup as bs
from core.models import *

#동물사랑, 퀸앤퍼피, 강아지왕국, 강아지대통령
brand_list=[]
pre_brand_selector=[]

def brand_crawling():
    #동물사랑APS
    html_text = requests.get('http://www.apslove.com/shop/goods/goods_list.php?category=006001').text
    soup = bs(html_text, 'html.parser')
    brand_list_1 = [i.getText() for i in soup.select('.category-sub-new tr:nth-of-type(1) ul a')]
    global brand_list
    brand_list += [brand_list_1]

    #퀸앤퍼피
    req = requests.get('http://queenpuppy.co.kr/shop/cate_main.html?category=182')
    req.encoding = 'euc-kr'
    html = req.text
    soup = bs(html, 'html.parser')
    brand_list_2 = [i.text.split(' ')[0] for i in soup.select('.cate a')]
    brand_list += [brand_list_2]

    #강아지왕국
    req = requests.get('http://www.dogskingdom.co.kr/shop/goods/goods_list.php?&category=001')
    req.encoding = 'euc-kr'
    html = req.text
    soup = bs(html, 'html.parser')
    brand_list_3 = [i.text.strip().split('(')[0].strip() for i in soup.select(".list_subcate a")]
    brand_list += [brand_list_3]

    #강아지대통령
    req = requests.get('http://www.dogpre.com/shop/goods/goods_list.php?category=036')
    req.encoding = 'euc-kr'
    html = req.text
    soup = bs(html, 'html.parser')
    brand_list_4 = [i.text.strip().split('(')[0] for i in soup.select('.nano-content.nano-content-scroll label')]
    global pre_brand_selector
    pre_brand_selector = soup.select('.nano-content.nano-content-scroll label input')
    brand_list += [brand_list_4]


def brand_create_first():
    #ASCII코드값 비교통한 brand 객체 생성 위해 오름차순 정렬
    for i in range(0, 3):
        brand_list[i].sort()

    #브랜드 객체 생성(brand4(강아지대통령)기준)
    for brand in brand_list[3]:
        Brand.objects.create(
            name=brand
        )


def brand_create():
    #brand이름 구분통해 객체생성여부 따지기
    brand_object = sorted(brand_list[3])
    for i in range(0, 3):
        index = 0
        for brand in brand_list[i]:
            for j in range(index, len(brand_object)):
                if brand==brand_object[j]:
                    index = j
                    break
                #아스키코드값 비교
                elif brand < brand_object[j]:
                    Brand.objects.create(
                        name=brand
                    )
                    brand_object.insert(j, brand)
                    index = j
                    break