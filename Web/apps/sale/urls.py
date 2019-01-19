# -*- coding: UTF-8 -*-

from django.urls import path
from . import views

app_name = 'sale'

urlpatterns = [
    path(
        r'goods_sale',
        views.GoodsSale.as_view(),
        name='goods_sale'
    ),
    path(
        r'order_list',
        views.OrderList.as_view(),
        name='order_list'
    ),
    path(
        r'order_detail',
        views.OrderDetail.as_view(),
        name='order_list'
    )
]
