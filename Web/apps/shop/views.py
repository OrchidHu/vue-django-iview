# -*- coding: UTF-8 -*-
import json

from django.contrib.auth import logout
from django.views.generic import View

import Web.apps.shop.models as model
from Utils.django_utils import  JsonError, JsonSuccess, redis_get, JsonReLogin, JsonForbid
from Web.apps.shop.forms import CreateGoodForm


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
                'id': data.id,
                'bar_id': data.bar_id,
                'name': data.name,
                'genre': data.genre,
                'buy_price': data.buy_price,
                'sale_price': data.sale_price,
                'supplier': data.supplier
            }
            ret.append(good_data)
        return ret

class CreateGood(View):
    """
    新建商品
    """

    def get(self, request):
        json_data = request.GET.get('data')
        data = json.loads(json_data)
        bar_id = data.get('bar_id')
        obj = model.Good.objects.filter(bar_id=bar_id).first()
        if obj:
            return JsonError("商品已存在")
        form = CreateGoodForm(data)
        if form.is_valid():
           form.save()
           good_id = form.instance.id
           return JsonSuccess("创建成功", id=good_id)
        else:
            for key in form.errors:
               return JsonError(form.errors[key][0])
        return JsonError("提交数据有误")


class UpdateGood(View):
    """
    更新商品
    """

    def get(self, request):
        json_data = request.GET.get('data')
        data = json.loads(json_data)
        good_id = data.get('id')
        is_exise = model.Good.objects.filter(bar_id=data.get('bar_id')).first()
        if is_exise and is_exise.id != good_id:
            return JsonError("该条码商品已存在")
        instance = model.Good.objects.filter(id=good_id).first()
        if instance:
            form = CreateGoodForm(data, instance=instance)
        else:
            form = CreateGoodForm(data)
        if form.is_valid():
            form.save()
            return JsonSuccess("创建成功")
        return JsonError("提交数据有误")


class Delete(View):
    """删除商品"""

    def get(self, request):
        import time
        time.sleep(0.5)
        json_data = request.GET.get('data')
        data = json.loads(json_data)
        if data['del_list']:
            for good in data.get('del_list'):
                try:
                    model.Good.objects.filter(id=good['id']).delete()
                except Exception:
                    return JsonError("删除失败", data=self.full_data())
            return JsonSuccess("删除成功", data=self.full_data())
        return JsonError("请选择需要删除的商品")

    def full_data(self):
        return Good.get_data(self)

