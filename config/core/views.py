import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
    required_products = product_all.filter(name__icontains=q)

    #brand 검색
    if required_brand.count() != 0:
        return render(request, 'core/search_result.html', {
            "required_brand": required_brand,
        })
    #keyword 검색
    else:
        result = keyword_detail(required_products)

        return render(request, 'core/keyword_detail.html', result)


def keyword_detail(products):
    similarity_group = similarity_test(products, 4)
    chart_index_1 = ["x"]
    mall0 = ["동물사랑APS"]
    mall1 = ["QueenNPuppy"]
    mall2 = ["kingdom"]
    mall3 = ['president']

    for sameProducts in similarity_group:
        check = [0, 0, 0, 0]
        chart_index_1 += [Product.objects.get(id=sameProducts[0]).name]
        for j in range(len(sameProducts)):
            product_include = str(Product.objects.get(id=sameProducts[j]).mall)

            if  product_include== '동물사랑APS':
                mall0 += [Product.objects.get(id=sameProducts[j]).stock]
                check[0] = 1
            if product_include == 'QueenNPuppy':
                mall1 += [Product.objects.get(id=sameProducts[j]).stock]
                check[1] = 1
            if product_include == 'kingdom':
                mall2 += [Product.objects.get(id=sameProducts[j]).stock]
                check[2] = 1
            if product_include == 'president':
                mall3 += [Product.objects.get(id=sameProducts[j]).stock]
                check[3] = 1
            print(check)
        for i in range(4):
            if check[i] == 0:
                if i == 0:
                    mall0.append(0)
                if i == 1:
                    mall1.append(0)
                if i == 2:
                    mall2.append(0)
                if i == 3:
                    mall3.append(0)



    return {"similarity_group": similarity_group,
            "chart_index_1": chart_index_1,
            "mall0": mall0,
            "mall1": mall1,
            "mall2": mall2,
            "mall3": mall3,
            }

def similarity_test(products, mallCount):

    product_id = []
    product_name = []
    #products와 같은 id의 상품 이름, id가져오기
    for product in products:
        product_id += [product.pk]
        product_name += [product.name]


    for i in range(len(product_name)):
        product_name[i] = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', product_name[i]).lower()
        product_name[i] = product_name[i].replace('유기농', '').replace('플러스', '')


    #id:상품명 -> 상품 pk찾기위해 딕셔녀리 생성
    product_dic = {}
    for i in range(len(product_dic)):
        product_dic[product_id[i]] = product_name[i]


    #jaccardDistance 유사도 측정
    similarity = {}
    product_list = []
    while(len(product_name) != 0):
        for i in range(len(product_name)):

            jaccard = 1 - (distance.jaccard(product_name[0], product_name[i]))
            similarity[product_id[i]] = jaccard

        similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
        product_list += [[pk for pk, sim in similarity[0: mallCount] if sim>=0.95]]


        for j in range(len(product_list[-1])):
            index = int(product_id.index(product_list[-1][j]))
            del product_id[index]
            del product_name[index]
            similarity={}

    return product_list

def brand_detail(request,pk):
    certain_brand = Brand.objects.get(id=pk)
    mall_of_certain_brand = certain_brand.malls.all()
    products_mall1 = []
    products_mall2 = []
    products_mall3 = []
    products_mall4 = []

    if certain_brand.malls.filter(name="동물사랑APS"):
        products_mall1 += certain_brand.malls.filter(name="동물사랑APS").first().products.all()
    if certain_brand.malls.filter(name="QueenNPuppy"):
        products_mall2 += certain_brand.malls.filter(name="QueenNPuppy").first().products.all()
    if certain_brand.malls.filter(name="kingdom"):
        products_mall3 += certain_brand.malls.filter(name="kingdom").first().products.all()
    if certain_brand.malls.filter(name="president"):
        products_mall4 += certain_brand.malls.filter(name="president").first().products.all()

    all_product = products_mall1 + products_mall2 + products_mall3 + products_mall4

    final_result = similarity_test(all_product, 4)

    chart_index_1 = ["x"]
    mall0 = ["동물사랑APS"]
    mall1 = ["QueenNPuppy"]
    mall2 = ["kingdom"]
    mall3 = ['president']

    for sameProducts in final_result:
        check = [0, 0, 0, 0]
        chart_index_1 += [Product.objects.get(id=sameProducts[0]).name]
        for j in range(len(sameProducts)):
            product_include = str(Product.objects.get(id=sameProducts[j]).mall)

            if  product_include== '동물사랑APS':
                mall0 += [Product.objects.get(id=sameProducts[j]).stock]
                check[0] = 1
            if product_include == 'QueenNPuppy':
                mall1 += [Product.objects.get(id=sameProducts[j]).stock]
                check[1] = 1
            if product_include == 'kingdom':
                mall2 += [Product.objects.get(id=sameProducts[j]).stock]
                check[2] = 1
            if product_include == 'president':
                mall3 += [Product.objects.get(id=sameProducts[j]).stock]
                check[3] = 1
            print(check)
        for i in range(4):
            if check[i] == 0:
                if i == 0:
                    mall0.append(0)
                if i == 1:
                    mall1.append(0)
                if i == 2:
                    mall2.append(0)
                if i == 3:
                    mall3.append(0)
    return render(request, "core/brand_detail.html", {
        "products_mall1": products_mall1,
        "products_mall2": products_mall2,
        "products_mall3": products_mall3,
        "products_mall4": products_mall4,
        'mall_of_certain_brand': mall_of_certain_brand,
        'final_result': final_result,
        'chart_index_1':chart_index_1,
        'mall0': mall0,
        'mall1': mall1,
        'mall2': mall2,
        'mall3': mall3,

    })






##################################################################################



# def similarity_test(products, mallCount):
#     product_id = []
#     product_name = []
#     product_all=[]
#     # products와 같은 id의 상품 이름, id가져오기
#     # for product in products:
#     #     product_id += [product.pk]
#     #     product_name += [product.name]
#     product_all = [product for product in products]
#     for i  in product_all:
#         i.name = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', i.name.lower())
#         i.name = i.name.replace('유기농', '').replace('플러스', '')
#
#     print(product_all)
#
#     # for i in range(len(product_name)):
#     #     product_name[i] = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', product_name[i]).lower()
#     #     product_name[i] = product_name[i].replace('유기농', '').replace('플러스', '')
#
#     # id:상품명 -> 상품 pk찾기위해 딕셔녀리 생성
#     # product_dic = {}
#     # for i in range(len(product_dic)):
#     #     product_dic[product_id[i]] = product_name[i]
#
#     # jaccardDistance 유사도 측정
#     similarity = {}
#     post_product_list = []
#     product_list = []
#     while (len(product_all) != 0):
#         for i in range(len(product_all)):
#             jaccard = 1 - (distance.jaccard(product_all[0].name, product_all[i].name))
#             similarity[product_all[i]] = jaccard
#
#
#         similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
#         for pk,sim in similarity:
#             if float(sim)>0.93:
#                 post_product_list.append(pk)
#         for i in post_product_list:
#             if i.mall == "동물사랑APS":
#                 product_list.append([i].stock)
#             elif i.mall == "QueenNPuppy":
#                 product_list.append([i].stock)
#             elif i.mall == "kingdom":
#                 product_list.append([i].stock)
#             elif i.mall == "president":
#                 product_list.append([i].stock)
#             else:
#                 product_list.append(0)
#         for j in range(len(product_list[-1])):
#             index = int(product_id.index(product_list[-1][j]))
#
#             del product_id[index]
#             del product_name[index]
#             similarity = {}
#
#     return product_list
# def brand_detail(request, pk):
#     certain_brand = Brand.objects.get(id=pk)
#     mall_of_certain_brand = certain_brand.malls.all()
#     # 가지고 있지 않는 몰 생각하기
#     mall_of_certain_brand_count = certain_brand.malls.all().count()
#     products_mall1 = []
#     products_mall2 = []
#     products_mall3 = []
#     products_mall4 = []
#
#     if certain_brand.malls.filter(name="동물사랑APS"):
#         products_mall1 += certain_brand.malls.get(name="동물사랑APS").products.all()
#     if certain_brand.malls.filter(name="QueenNPuppy"):
#         products_mall2 += certain_brand.malls.get(name="QueenNPuppy").products.all()
#     if certain_brand.malls.filter(name="kingdom"):
#         products_mall3 += certain_brand.malls.get(name="kingdom").products.all()
#     if certain_brand.malls.filter(name="president"):
#         products_mall4 += certain_brand.malls.get(name="president").products.all()
#
#     all_product = products_mall1 + products_mall2 + products_mall3 + products_mall4
#
#     final_result = similarity_test(all_product, mall_of_certain_brand_count)
#     hooah = []
#     chart_index_1 = ["x"]
#     mall0 = ["동물사랑APS"]
#     mall1 = ["QueenNPuppy"]
#     mall2 = ["kingdom"]
#     mall3 = ['president']
#     for i in final_result:
#         for j in range(len(i)):
#             hooah += [[Product.objects.get(id=i[j]).mall]]
#     for h in final_result:
#         for j in range(len(h)):
#             if j == 0:
#                 chart_index_1 += [Product.objects.get(id=h[j]).name]
#                 mall0 += [Product.objects.get(id=h[j]).stock]
#             if j == 1:
#                 mall1 += [Product.objects.get(id=h[j]).stock]
#             if j == 2:
#                 mall2 += [Product.objects.get(id=h[j]).stock]
#             if j == 3:
#                 mall3 += [Product.objects.get(id=h[j]).stock]
#
#     return render(request, "core/brand_detail.html", {
#         "products_mall1": products_mall1,
#         "products_mall2": products_mall2,
#         "products_mall3": products_mall3,
#         "products_mall4": products_mall4,
#         'mall_of_certain_brand': mall_of_certain_brand,
#         'final_result': final_result,
#         'chart_index_1': chart_index_1,
#         'mall0': mall0,
#         'mall1': mall1,
#         'mall2': mall2,
#         'mall3': mall3,

    # })


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


def logout(request):
    auth.logout(request)
    return redirect('core:home')


@login_required
def reset_pw(request):
    context = {}
    if request.method == "POST":
        current_password = request.POST.get("original_password")
        user = request.user
        if check_password(current_password, user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("core:home")
            else:
                context.update({'error': "새로운 비밀번호를 다시 확인해주세요."})
        else:
            context.update({'error': "현재 비밀번호가 일치하지 않습니다."})
    return render(request, "core/reset_pw.html", context)


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


@login_required
def delete_account(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get("password1") == request.POST.get("password2"):
            username = request.POST.get("delete_username")
            password = request.POST.get("password1")
            user = request.user
            if check_password(password, user.password) and username == user.username:
                request.user.delete()
                return redirect('core:login')
            else:
                context.update({'error': "아이디와 비밀번호를 확인해주세요."})
        else:
            context.update({'error': "입력하신 비밀번호가 일치하지 않습니다."})
    return render(request, 'core/delete_account.html', context)


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        profile = request.user.profile  # 로그인한 유저의 프로필을 가져온다.
        product_id = request.POST.get('pk', None)
        product = Product.objects.get(pk=product_id)  # 해당 메모 오브젝트를 가져온다

        if product.likes.filter(id=profile.id).exists():  # 이미 해당 유저가 likes컬럼에 존재하면
            product.likes.remove(profile)  # likes 컬럼에서 해당 유저를 지운다.
            message = 'You disliked this'
        else:
            product.likes.add(profile)
            message = 'You liked this'
        context = {'likes_count': product.total_likes, 'message': message}
        return HttpResponse(json.dumps(context), content_type='application/json')
        # dic 형식을 json 형식으로 바꾸어 전달한다.
def logout(request):
    auth.logout(request)
    return redirect('core:home')
