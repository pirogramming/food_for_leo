from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.models import Product


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