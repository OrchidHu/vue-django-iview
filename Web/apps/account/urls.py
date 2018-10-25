# -*- coding: UTF-8 -*-

from django.urls import path
from . import views

app_name = 'account'

urlpatterns =[
    path(
        r'login/',
        views.Login.as_view(),
        name='login'
    )
]