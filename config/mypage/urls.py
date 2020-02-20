from django.contrib import admin
from django.urls import path, include

from mypage.views import *

app_name = 'mypage'

urlpatterns = [
    path('profile/', update_profile, name='profile'),
    path('name_update/', name_update, name='name_update'),
    path('email_update/', email_update, name='email_update'),
    path('tel_update/', tel_update, name='tel_update'),

    path('pet_list/', pet_list, name='pet_list'),
    path('pet/create/', create_pet, name='create_pet'),
    path('pet/detail/<int:pk>/', pet_detail, name='pet_detail'),
    path('pet/detail/<int:pk>/edit/', pet_update, name='pet_update'),
    path('pet/detail/<int:pk>/delete/', pet_delete, name='pet_delete'),

    path('pet/brief/', pet_brief, name='pet_brief'),


    path('favorites/', favorites, name='favorites'),

    path('diary_list/', diary_list, name='diary_list'),
    path('diary/create/', create_diary, name='create_diary'),
    path('diary/detail/<int:pk>/', detail_diary, name='detail_diary'),
    path('diary/detail/<int:pk>/edit/', update_diary, name='update_diary'),
    path('diary/detail/<int:pk>/delete/', delete_diary, name='delete_diary'),
]