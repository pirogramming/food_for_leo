from django.contrib import admin
from django.urls import path, include

from core.views import *

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('brand_page/', brand_page, name='brand_page'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('sign_up', sign_up, name='sign_up'),
    path('product_list/', product_list, name='product_list'),
    path('result/',search_result, name="search_result"),
    path('brand/detail/<int:pk>',brand_detail, name='brand_detail'),
]