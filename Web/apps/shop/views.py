# -*- coding: UTF-8 -*-
import json

from django.contrib.auth import logout
from django.views.generic import View
from Utils.django_utils import  JsonError, JsonSuccess, redis_get, JsonReLogin, JsonForbid


class Good(View):

    def get(self, request):
        user = request.user
        token = request.COOKIES.get("token")
        db_token = redis_get(user.username)
        if not db_token or db_token != token:
            logout(request)
            return JsonReLogin('需要身份验证')
        if user.is_staff:
            return JsonSuccess("请求成功")
        return JsonForbid('没有权限')


