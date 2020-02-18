from django.contrib import admin
from django.urls import path, include

from mypage.views import *

app_name = 'mypage'

urlpatterns = [
    path('profile/', update_profile, name='profile'),
    path('create_pet/', create_pet, name='create_pet'),
    path('pet_info/', pet_info, name='pet_info'),
    path('email_update/', email_update, name='email_update'),
    path('tel_update/', tel_update, name='tel_update'),

    path('favorites/', favorites, name='favorites'),

    path('diary/', diary, name='diary'),
    path('diary/create/', create_diary, name='create_diary'),
    path('diary/detail/<int:pk>/', detail_diary, name='detail_diary'),
]