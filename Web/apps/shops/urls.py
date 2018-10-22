# -*- coding: UTF-8 -*-
from django.conf.urls import  url

from . import views

app_name = 'shops'

urlpatterns =[
    url(
        r'^$',
        views.Login.as_view(),
        name='login'
    ),

    # url(
    #     r'^client_manage/$',
    #     views.ClientManage.as_view(),
    #     name='client_manage'
    # ),

]
