import os
import sys

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

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
import random


def search_result(request):
    product_all = Product.objects.all()
    brand_all = Brand.objects.all()
    q = request.GET.get('q', '')

    required_brand = brand_all.filter(name__icontains=q)
    required_products = product_all.filter(name__icontains=q)

    # brand 검색
    if required_brand.count() != 0:
        return render(request, 'core/search_result.html', {
            "required_brand": required_brand,
        })
    # keyword 검색
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

    item_final = []
    for sameProducts in similarity_group:
        check = [0, 0, 0, 0]
        chart_index_1 += [Product.objects.get(id=sameProducts[0]).name]
        item_final += [Product.objects.get(id=sameProducts[0])]
        for j in range(len(sameProducts)):
            product_include = str(Product.objects.get(id=sameProducts[j]).mall)

            if product_include == '동물사랑APS':
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

    mall_length = len(mall0)

    return {"similarity_group": similarity_group,
            "item_final": item_final,
            "chart_index_1": chart_index_1,
            "mall0": mall0,
            "mall1": mall1,
            "mall2": mall2,
            "mall3": mall3,
            "mall_length": mall_length,
            }


def item_House(request):
    itemsAll = list(Product.objects.all())
    random.shuffle(itemsAll)
    itemsRand = itemsAll[:50]

    page = request.GET.get('page', 1)
    paginator = Paginator(itemsRand, 16)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'core/item_House.html', {
        "items": items,
    })


def similarity_test(products, mallCount):
    product_id = []
    product_name = []
    # products와 같은 id의 상품 이름, id가져오기
    for product in products:
        product_id += [product.pk]
        product_name += [product.name]

    for i in range(len(product_name)):
        product_name[i] = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', product_name[i]).lower()
        product_name[i] = product_name[i].replace('유기농', '').replace('플러스', '').replace("eco", "에코")

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
        product_list += [[pk for pk, sim in similarity[0: mallCount] if sim >= 0.95]]

        for j in range(len(product_list[-1])):
            index = int(product_id.index(product_list[-1][j]))
            del product_id[index]
            del product_name[index]
            similarity = {}

    return product_list


def brand_page(request):
    brands_mall1 = []
    brands_mall2 = []
    brands_mall3 = []
    brands_mall4 = []

    brands_mall1 += Brand.objects.filter(malls__name="동물사랑APS").all()
    brands_mall2 += Brand.objects.filter(malls__name="QueenNPuppy").all()
    brands_mall3 += Brand.objects.filter(malls__name="kingdom").all()
    brands_mall4 += Brand.objects.filter(malls__name="president").all()
    itemsAll=list(Product.objects.all())
    random.shuffle(itemsAll)
    itemsRand = itemsAll[:50]


    page = request.GET.get('page', 1)
    paginator = Paginator(itemsRand, 16)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, "core/brand_page.html", {
        "itemsAll_random" : itemsRand,
        "items":items,
        "brands_mall1":brands_mall1,
        "brands_mall2": brands_mall2,
        "brands_mall3": brands_mall3,
        "brands_mall4": brands_mall4,

    })


def product_detail(request, pk):
    brands_mall1 = []
    brands_mall2 = []
    brands_mall3 = []
    brands_mall4 = []

    brands_mall1 += Brand.objects.filter(malls__name="동물사랑APS").all()
    brands_mall2 += Brand.objects.filter(malls__name="QueenNPuppy").all()
    brands_mall3 += Brand.objects.filter(malls__name="kingdom").all()
    brands_mall4 += Brand.objects.filter(malls__name="president").all()

    certain_product =Product.objects.get(id=pk)
    certain_product.name = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', certain_product.name).lower()
    certain_product.name = certain_product.name.replace('유기농', '').replace('플러스', '').replace('eco',"에코")
    product_all =Product.objects.all()
    for i in product_all:
        i.name = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'… ]+', '', i.name).lower()
        i.name = i.name.replace('유기농', '').replace('플러스', '')
    similarity = {}
    product_list = []
    for i in product_all:
        jaccard = 1 - (distance.jaccard(certain_product.name, i.name))
        similarity[i.id] = jaccard
    similarity = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)
    product_list += [[pk for pk, sim in similarity[0:4] if sim >= 0.95]]
    chart_index_1 = ["x"]
    mall0 = ["동물사랑APS"]
    mall1 = ["QueenNPuppy"]
    mall2 = ["kingdom"]
    mall3 = ['president']
    for sameProducts in product_list:
        check = [0, 0, 0, 0]
        print(sameProducts)
        chart_index_1 += [Product.objects.get(id=sameProducts[0]).name]
        for j in range(len(sameProducts)):
            product_include = str(Product.objects.get(id=sameProducts[j]).mall)

            if product_include == '동물사랑APS':
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
    mall_length = len(product_list)
    final_result_revised = []
    final_result_revised_stock_check=0
    for i in product_list[0]:
        final_result_revised.append(Product.objects.get(id=i))
    final_result_revised_detail = final_result_revised[0].img_detail
    for i in final_result_revised:
        if i.stock!=0:
            final_result_revised_stock_check=1


    return render(request, 'core/product_detail.html', {
        'chart_index_1': chart_index_1,
        'mall0': mall0,
        'mall1': mall1,
        'mall2': mall2,
        'mall3': mall3,
        'mall_length': mall_length,
        'final_result_revised': final_result_revised,
        "brands_mall1": brands_mall1,
        "brands_mall2": brands_mall2,
        "brands_mall3": brands_mall3,
        "brands_mall4": brands_mall4,
        'final_result_revised_detail': final_result_revised_detail,
        'final_result_revised_stock_check' : final_result_revised_stock_check,
    })


def brand_detail(request, pk):
    brand_all = Brand.objects.all()
    product_all = Product.objects.all()
    brands_mall1 = []
    brands_mall2 = []
    brands_mall3 = []
    brands_mall4 = []

    brands_mall1 += Brand.objects.filter(malls__name="동물사랑APS").all()
    brands_mall2 += Brand.objects.filter(malls__name="QueenNPuppy").all()
    brands_mall3 += Brand.objects.filter(malls__name="kingdom").all()
    brands_mall4 += Brand.objects.filter(malls__name="president").all()

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
    final_result_sort = {}
    for i in range(len(final_result)):
        final_result_sort[str(final_result[i])] = len(final_result[i])
    final_result = ["".join(list(i[0])[1:-1]).split(", ") for i in sorted(final_result_sort.items(), key=operator.itemgetter(1), reverse=True)]
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

            if product_include == '동물사랑APS':
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
    mall_length = len(final_result)
    final_result_revised = []
    for i in final_result:
        final_result_revised.append(Product.objects.get(id=i[0]))

    return render(request, "core/brand_detail.html", {
        "products_mall1": products_mall1,
        "products_mall2": products_mall2,
        "products_mall3": products_mall3,
        "products_mall4": products_mall4,
        "brands_mall1": brands_mall1,
        "brands_mall2": brands_mall2,
        "brands_mall3": brands_mall3,
        "brands_mall4": brands_mall4,
        'mall_of_certain_brand': mall_of_certain_brand,
        'final_result': final_result,
        'chart_index_1': chart_index_1,
        'mall0': mall0,
        'mall1': mall1,
        'mall2': mall2,
        'mall3': mall3,
        'mall_length': mall_length,
        'final_result_revised': final_result_revised,
    })


def home(request):
    return render(request, 'core/home.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('core:home')
        else:
            return render(request, 'core/home.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'core/login.html')



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
    return redirect('core:login')
