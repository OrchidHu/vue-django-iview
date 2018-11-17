# -*- coding: UTF-8 -*-
import json
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.views.generic import View
from Utils.django_utils import  JsonError, JsonSuccess, get_token, redis_get, redis_db
from Web.models import XYUser

class Login(View):
    """ 登录 """

    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            data = json.loads(request.body.decode("utf-8"))
        username = data.get('username')
        password = data.get('password')
        # next_url = request.GET.get('next') or resolve_url("admin")
        # if user.is_active is false then can't use authenticate() to validate
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            ret = {'username': username}
            token = redis_get(username)
            if not token:
                token = get_token()
                redis_db.setex(username, token, 30000)
            session_id = request.session.session_key
            ret['token'] = token
            ret['session_id'] = session_id
            ret['avator'] = user.avatar.name if user.avatar else None
            return JsonSuccess('登录成功', **ret)
        user = XYUser.objects.filter(username=username).first()
        if not user:
            return JsonError('用户名未注册')
        if user.is_active is False:
            return JsonError('账号未激活')
        return JsonError('账号密码不正确')


class Logout(LogoutView):

    def get(self, request):
        logout(request)
        return JsonSuccess("退出成功")

