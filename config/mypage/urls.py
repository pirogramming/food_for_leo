from django.contrib import admin
from django.urls import path, include

from mypage.views import profile, pet_profile, favorites, diary

app_name = 'mypage'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('pet_profile/', pet_profile, name='pet_profile'),
    path('favorites/', favorites, name='favorites'),
    path('diary/', diary, name='diary'),
]