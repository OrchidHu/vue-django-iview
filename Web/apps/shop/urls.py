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
        r'scan_stock_search',
        views.ScanStockSearch.as_view(),
        name='scan_stock_search'
    ),
    path(
        r'create_stock_in_record',
        views.GoodStockRecord.as_view(),
        name='create_stock_in_record'
    ),
    path(
        r'get_exam_task',
        views.ExamTaskList.as_view(),
        name='get_exam_task'
    ),
    path(
        r'commit_exam_task',
        views.CommitExamTask.as_view(),
        name='commit_exam_task'
    ),
    path(
        r'shop_list',
        views.ShopList.as_view(),
        name='shop_list'
    ),
    path(
        r'search_stock_report',
        views.SearchStockReport.as_view(),
        name='search_stock_report'
    ),
    path(
        r'scan_sale_search',
        views.ScanSaleSearch.as_view(),
        name='scan_sale_search'
    ),
    path(
        r'search_good_sale',
        views.SearchGoodSale.as_view(),
        name='search_good_sale'
    )
]
