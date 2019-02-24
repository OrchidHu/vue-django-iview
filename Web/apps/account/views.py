# -*- coding: UTF-8 -*-
import json
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.views.generic import View
from Utils.django_utils import JsonError, JsonSuccess, get_token, redis_get, redis_db, ArgsMixin
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
            ret['avator'] = user.avatar.name if user.avatar else ''
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


class Register(ArgsMixin, View):
    """注册"""

    def post(self, request):
        username = self.get_arg('username').strip()
        password = self.get_arg('password')
        user = XYUser.objects.filter(username=username).first()
        if user:
            return JsonError("用户名已存在")
        if not self.valid_password(password):
            return JsonError("输入的密码不合法")
        user = XYUser.objects.create(username=username)
        user.set_password(password)
        user.save()
        return JsonSuccess("注册成功")

    def valid_password(self, password):
        if len(password) not in range(6, 17):
            return False
        for word in password:
            if not word.isdigit() and not word.isalpha() and word not in '_,.*&^%$#@!`?':
                return False
        return True

