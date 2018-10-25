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
]
