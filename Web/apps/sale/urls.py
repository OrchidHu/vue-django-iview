# -*- coding: UTF-8 -*-

from django.urls import path
from . import views

app_name = 'sale'

urlpatterns = [
    path(
        r'goods_sale',
        views.GoodsSale.as_view(),
        name='goods_sale'
    )
]
