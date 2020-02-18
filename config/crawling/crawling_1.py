import pandas as pd
import re
import distance
import operator

def similarity_test(products, mallCount):
    df = pd.read_csv("/Users/kang/Downloads/programming/dev/food_for_LEO/config/crawling", encoding="CP949")

    #products와 같은 id의 상품 이름, id가져오기
    for product in products:
        product_id = + df['id' == product.id]
        product_name = + df['name' == product.name]

    for i in range(len(product_name)):
        product_name[i] = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', product_name[i]).lower()
        product_name[i] = product_name[i].replace('유기농', '').replace('플러스', '')

    #id:상품명 -> 상품 pk찾기위해 딕셔녀리 생성
    product_dic = {}
    for i in range(len(product_name)):
        product_dic[product_id[i]] = product_name[i]

    #jaccardDistance 유사도 측정
    similarity = {}
    product_list = []
    while(len(product_name) != 0):
        for i in range(product_name):
            jaccard = 1 - (distance.jaccard(product_name[0], product_name[i]))
            similarity[product_id[i]] = jaccard
        similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
        product_list += [list(similarity.keys())[0: 3]]
        for i in range(len(product_list[-1])):
            index = product_id.index(product_list[-1][i])
            del product_id[index]
            del product_name[index]

    return product_list

if __name__ == '__main__':