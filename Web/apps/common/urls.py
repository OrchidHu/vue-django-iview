# -*- coding: UTF-8 -*-

from django.urls import path
from . import views

app_name = 'common'

urlpatterns =[
    path(
        r'quantify_list/',
        views.QuantifyList.as_view(),
        name='quantify_list'
    ),
    path(
        r'supplier_list',
        views.SupplierList.as_view(),
        name='supplier_list'
    )
]