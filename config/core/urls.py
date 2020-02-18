from django.contrib import admin
from django.urls import path, include

from core.views import *

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('brand_page/', brand_page, name='brand_page'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('reset_pw', reset_pw, name='reset_pw'),
    path('sign_up', sign_up, name='sign_up'),
    path('account/delete/', delete_account, name='delete_account'),
    path('product/detail/', product_detail, name='product_detail'),
    path('like/', like, name='like'),  #여기 <int:pk>/ 들어가는지 아닌지 모르겠...ㅎㅎ
    path('product_list/', product_list, name='product_list'),
    path('result/',search_result, name="search_result"),
    path('brand/detail/<int:pk>',brand_detail, name='brand_detail'),
    path("product/detail/", search_result_product, name="search_result_product"),

]