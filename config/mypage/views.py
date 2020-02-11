from django.shortcuts import render


def profile(request):
    return render(request, 'mypage/profile.html')


def pet_profile(request):
    return render(request, 'mypage/pet_profile.html')


def favorites(request):
    return render(request, 'mypage/favorites.html')


def diary(request):
    return render(request, 'mypage/diary.html')