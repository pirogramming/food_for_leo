from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from core.models import Product

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


def brand_detail(request, pk):
    certain_brand = Brand.objects.get(id=pk)
    mall_of_certain_brand = certain_brand.malls.all()
    products_mall1 = []
    products_mall2 = []
    products_mall3 = []
    products_mall4 = []
    product_2=[]
    product_3 = []
    product_4 = []
    if certain_brand.malls.filter(name="동물사랑APS"):
        products_mall1 += certain_brand.malls.filter(name="동물사랑APS").first().products.all()
    if certain_brand.malls.filter(name="queen"):
        products_mall2 += certain_brand.malls.filter(name="mall1").first().products.all()
    if certain_brand.malls.filter(name="kingdom"):
        products_mall3 += certain_brand.malls.filter(name="kingdom").first().products.all()
    if certain_brand.malls.filter(name="president"):
        products_mall4 += certain_brand.malls.filter(name="president").first().products.all()
    for i in products_mall1:
        product_2 +=certain_brand.malls.filter(name="mall1").first().products.all().filter(name=i.name.split(' ')[-4:-1])
        product_3 +=certain_brand.malls.filter(name="kingdom").first().products.all().filter(name=i.name.split(' ')[-4:-1])
        product_4 += certain_brand.malls.filter(name="president").first().products.all().filter(name=i.name.split(' ')[-4:-1])
    return render(request, "core/brand_detail.html", {
        "products_mall1": products_mall1,
        "products_mall2": products_mall2,
        "products_mall3": products_mall3,
        "products_mall4": products_mall4,
        'mall_of_certain_brand': mall_of_certain_brand,
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