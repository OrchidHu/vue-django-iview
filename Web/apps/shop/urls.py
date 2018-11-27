# -*- coding: UTF-8 -*-

from django.urls import path
from . import views

app_name = 'shops'

urlpatterns =[
    path(
        r'good/',
        views.Good.as_view(),
        name='good'
    ),
    path(
        r'create_good',
        views.CreateGood.as_view(),
        name='create_good'
    ),
    path(
        r'update_good',
        views.UpdateGood.as_view(),
        name='update_good'
    ),
    path(
        r'delete_good',
        views.Delete.as_view(),
        name='delete_good'
    ),
    path(
        r'other_package_list',
        views.OtherPackageList.as_view(),
        name='other_package_list'
    ),
    path(
        r'other_package',
        views.OtherPackage.as_view(),
        name='other_package'
    ),
    path(
        r'scan_search',
        views.ScanSearch.as_view(),
        name='scan_search'
    )
]
