# -*- coding: UTF-8 -*-
import json

from django.contrib.auth import authenticate, login
from django.views.generic import View
from Utils.django_utils import  JsonError, JsonSuccess, get_token, redis_get, redis_db

class Login(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username',1)
        password = data.get('password',1)
        # next_url = request.GET.get('next') or resolve_url("admin")
        user = authenticate(username=username, password=password)
        ret = {'username': username}
        if user and user.is_active:
            token = redis_get(username)
            if not token:
                token = get_token()
                redis_db.setex(username, token, 300)
            login(request, user)
            session_id = request.session.session_key
            ret['token'] = token
            ret['session_id'] = session_id
            return JsonSuccess('登录成功', **ret)
        if user and not user.is_active:
            return JsonError('账号被冻结')
        return JsonError('用户名密码不正确')