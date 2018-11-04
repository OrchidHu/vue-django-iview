# -*- coding: UTF-8 -*-
import json

from django.contrib.auth import logout
from django.views.generic import View

import Web.apps.shop.models as model
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
            data = self.get_data()
            return JsonSuccess("请求成功", data=data)
        return JsonForbid('没有权限')

    def get_data(self):
        query_data =  model.Good.objects.all()
        ret = []
        if not query_data:
            return ret
        for data in query_data:
            good_data = {
                'bar_id': data.bar_id,
                'name': data.name,
                'genre': data.genre,
                'buy_price': data.buy_price,
                'sale_price': data.sale_price,
                'supplier': data.supplier
            }
            ret.append(good_data)
        return ret

