import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from core.models import *
import distance
import re
import operator
import pandas as pd


def product_list(request):
    product_all = Product.objects.all()
    brand_all = Brand.objects.all()
    q = request.GET.get('q', '')
    if q:
        product_all = product_all.filter(name__icontains=q)
    return render(request, 'core/product_list.html', {
        'product_list': product_all,

    })


def search_result(request):
    product_all = Product.objects.all()
    brand_all = Brand.objects.all()
    q = request.GET.get('q', '')

    required_brand = brand_all.filter(name__icontains=q)

    return render(request, 'core/search_result.html', {
        "required_brand": required_brand,
    })


import re
import distance
import operator


def similarity_test(products, mallCount):
    product_id = []
    product_name = []
    product_all=[]
    # products와 같은 id의 상품 이름, id가져오기
    for product in products:
        product_id += [product.pk]
        product_name += [product.name]
    product_all = [product for product in products]
    for i  in product_all:
        i.name = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', i.name.lower())
        i.name = i.name.replace('유기농', '').replace('플러스', '')
        print(i.name)
    print(product_all)

    for i in range(len(product_name)):
        product_name[i] = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', product_name[i]).lower()
        product_name[i] = product_name[i].replace('유기농', '').replace('플러스', '')

    # id:상품명 -> 상품 pk찾기위해 딕셔녀리 생성
    product_dic = {}
    for i in range(len(product_dic)):
        product_dic[product_id[i]] = product_name[i]

    # jaccardDistance 유사도 측정
    similarity = {}
    product_list = []
    while (len(product_name) != 0):

        for i in range(len(product_name)):
            jaccard = 1 - (distance.jaccard(product_name[0], product_name[i]))
            similarity[product_id[i]] = jaccard

        similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
        product_list += [[pk for pk, sim in similarity[0: mallCount]]]

        for j in range(len(product_list[-1])):
            index = int(product_id.index(product_list[-1][j]))

            del product_id[index]
            del product_name[index]
            similarity = {}

    return product_list


def brand_detail(request, pk):
    certain_brand = Brand.objects.get(id=pk)
    mall_of_certain_brand = certain_brand.malls.all()
    # 가지고 있지 않는 몰 생각하기
    mall_of_certain_brand_count = certain_brand.malls.all().count()
    products_mall1 = []
    products_mall2 = []
    products_mall3 = []
    products_mall4 = []

    if certain_brand.malls.filter(name="동물사랑APS"):
        products_mall1 += certain_brand.malls.get(name="동물사랑APS").products.all()
    if certain_brand.malls.filter(name="QueenNPuppy"):
        products_mall2 += certain_brand.malls.get(name="QueenNPuppy").products.all()
    if certain_brand.malls.filter(name="kingdom"):
        products_mall3 += certain_brand.malls.get(name="kingdom").products.all()
    if certain_brand.malls.filter(name="president"):
        products_mall4 += certain_brand.malls.get(name="president").products.all()

    all_product = products_mall1 + products_mall2 + products_mall3 + products_mall4

    final_result = similarity_test(all_product, mall_of_certain_brand_count)
    hooah = []
    chart_index_1 = ["x"]
    mall0 = ["동물사랑APS"]
    mall1 = ["QueenNPuppy"]
    mall2 = ["kingdom"]
    mall3 = ['president']
    for i in final_result:
        for j in range(len(i)):
            hooah += [[Product.objects.get(id=i[j]).mall]]
    for h in final_result:
        for j in range(len(h)):
            if j == 0:
                chart_index_1 += [Product.objects.get(id=h[j]).name]
                mall0 += [Product.objects.get(id=h[j]).stock]
            if j == 1:
                mall1 += [Product.objects.get(id=h[j]).stock]
            if j == 2:
                mall2 += [Product.objects.get(id=h[j]).stock]
            if j == 3:
                mall3 += [Product.objects.get(id=h[j]).stock]

    return render(request, "core/brand_detail.html", {
        "products_mall1": products_mall1,
        "products_mall2": products_mall2,
        "products_mall3": products_mall3,
        "products_mall4": products_mall4,
        'mall_of_certain_brand': mall_of_certain_brand,
        'final_result': final_result,
        'chart_index_1': chart_index_1,
        'mall0': mall0,
        'mall1': mall1,
        'mall2': mall2,
        'mall3': mall3,

    })
def search_result_product(request):
    product_all = Product.objects.all()

    q = request.GET.get('q', '')

    product_all_revised = product_all.filter(name__icontains=q)
    return render(request, 'core/search_result_product.html',{
        "product_all_revised":product_all_revised
    })

def home(request):
    return render(request, 'core/home.html')


def brand_page(request):
    return render(request, 'core/brand_page.html')


def product_detail(request):
    return render(request, 'core/product_detail.html')


def product_list(request):
    return render(request, 'core/product_list.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('core:login')
        else:
            return render(request, 'core/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'core/login.html')


def sign_up(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('core:home')
        return render(request, 'core/sign_up.html')
    else:
        return render(request, 'core/sign_up.html')


def logout(request):
    auth.logout(request)
    return redirect('core:home')
