# -*- coding: UTF-8 -*-
import json

from django.contrib.auth import authenticate, login
from django.shortcuts import resolve_url
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from Utils.db_connections import get_redis
from Utils.django_utils import parse_put, ArgsMixin, JsonError, JsonSuccess, get_token, redis_get, redis_db
from Web.models import XYUser


class Login(TemplateView):
    template_name = "login.html"

    # @csrf_protect
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username',1)
        password = data.get('password',1)
        # next_url = request.GET.get('next') or resolve_url("admin")
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            if user.has_perm("is_staff"):
                token = redis_get(username)
                if not token:
                    token = get_token()
                    redis_db.setex(username, token, 300)
                return JsonSuccess('登录成功', token=token)
            # return JsonSuccess('', redirect=next_url)
            return JsonError("权限不够")
        return JsonError('用户名密码不正确')

