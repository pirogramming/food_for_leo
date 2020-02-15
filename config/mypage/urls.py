from django.contrib import admin
from django.urls import path, include

from mypage.views import *

app_name = 'mypage'

urlpatterns = [
    path('profile/', update_profile, name='profile'),
    path('favorites/', favorites, name='favorites'),
    path('diary/', diary, name='diary'),
]