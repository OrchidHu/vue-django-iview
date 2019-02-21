# -*- coding: UTF-8 -*-

from django.urls import path
from . import views

app_name = 'account'

urlpatterns =[
    path(
        r'register',
        views.Register.as_view(),
        name='register'
    ),
    path(
        r'login/',
        views.Login.as_view(),
        name='login'
    ),
    path(
        r'logout',
        views.Logout.as_view(),
        name='logout'
    )
]