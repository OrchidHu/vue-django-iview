# -*- coding: UTF-8 -*-
import json

from django.contrib.auth import logout
from django.views.generic import View

import Web.apps.shop.models as model
from Utils.db_connections import get_redis
from Utils.django_utils import JsonError, JsonSuccess, redis_get, JsonReLogin, JsonForbid, get_genre_parent_id
from Web.apps.shop.forms import CreateGoodForm, CreateOtherPackageForm


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

            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            from asgiref.sync import async_to_sync
            c_name = redis_get("sock" + user.username)
            print(c_name, "shangxin")
            async_to_sync(channel_layer.send)(c_name, {"type": "send.message", "text": "你好啊"})
            return JsonSuccess("请求成功", data=data)
        return JsonForbid('没有权限')

    def get_data(self):
        query_data = model.Good.objects.all()
        ret = []
        if not query_data:
            return ret
        for data in query_data:
            good_data = {
                'id': data.id,
                'bar_id': data.bar_id,
                'name': data.name,
                'genre': data.genre.title if data.genre else '-',
                'genre_id': get_genre_parent_id(data.genre),
                'quantify': data.quantify.name if data.quantify else '-',
                'quantify_id': data.quantify.id if data.quantify else None,
                'buy_price': data.buy_price,
                'sale_price': data.sale_price,
                'supplier': data.supplier.name if data.supplier else '-',
                'supplier_id': data.supplier.id if data.supplier else None
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
        form_data = data['form']
        package_data = data['package_data']
        bar_id = form_data.get('bar_id')
        obj = model.Good.objects.filter(bar_id=bar_id).first()
        if obj:
            return JsonError("商品已存在")
        form = CreateGoodForm(form_data)
        if form.is_valid():
            good = form.save(commit=False)
            good.supplier_id = form_data['supplier_id']
            good.quantify_id = form_data['quantify_id']
            good.genre_id = form_data['genre_id'][-1] if form_data['genre_id'] else None
            try:
                good.save()
            except Exception:
                return JsonError("新建失败")
            good_id = form.instance.id
            for em in package_data:
                package_form = CreateOtherPackageForm(em)
                if not package_form.is_valid():
                    return JsonError(package_form.errors)
                if not valid_package(good, em):
                    good.delete()
                    return JsonError("包装价格不能低于成本价")
                other_package = package_form.save(commit=False)
                other_package.one_package_id = good_id
                other_package.quantify_id = em['quantify_id']
                other_package.save()
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
            good = form.save(commit=False)
            good.supplier_id = data['supplier_id']
            good.quantify_id = data['quantify_id']
            good.genre_id = data['genre_id'][-1] if data['genre_id'] else None
            good.save()
            return JsonSuccess("保存成功")
        return JsonError("提交数据有误")


class Delete(View):
    """删除商品"""

    def get(self, request):
        import time
        time.sleep(0.8)
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


class OtherPackageList(View):
    """商品其他包装数据"""

    def get(self, request):
        try:
            json_data = request.GET.get('data')
            data = json.loads(json_data)
        except Exception:
            return JsonError("解析失败")
        query_set = model.GoodPackage.objects.filter(one_package_id=data).all()
        if not query_set:
            return JsonSuccess("没有数据")
        ret = []
        for data in query_set:
            ret.append({
                'id': data.id,
                'bar_id': data.bar_id,
                'name': data.name,
                'quantify': data.quantify.name if data.quantify else "-",
                'quantify_id': data.quantify.id if data.quantify else None,
                'number': data.number,
                'package_price': data.package_price
            })
        return JsonSuccess("成功", data=ret)


class OtherPackage(View):
    """"添加其他包装"""

    def get(self, request):
        try:
            json_data = request.GET.get('data')
            data = json.loads(json_data)
        except Exception:
            return JsonError("解析失败")
        print(data)
        if data:
            if data.get("delete_id"):
                model.GoodPackage.objects.filter(id=data['delete_id']).delete()
                return JsonSuccess("删除成功")
            instance = model.Good.objects.filter(id=data['good_id']).first()
            if not instance:
                return JsonError("未知商品")
            form = CreateOtherPackageForm(data)
            if form.is_valid():
                if valid_package(instance, data):
                    package = form.save(commit=False)
                    package.one_package_id = data['good_id']
                    package.quantify_id = data['quantify_id']
                    package.save()
                    ret = {"package_id": package.id}
                    return JsonSuccess("添加成功", data=ret)
                else:
                    return JsonError("包装价格不能低于成本价")
            else:
                for key in form.errors:
                    return JsonError(form.errors[key][0])
            return JsonError("提交数据有误")


def valid_package(instance, data):
    cost_price = instance.buy_price * int(data['number'])
    if float(cost_price) > float(data['package_price']):
        return False
    return True


class ScanSearch(View):
    """扫码搜索"""

    def get(self, request):
        bar_id = request.GET.get('data')
        instance = model.Good.objects.filter(bar_id=bar_id).first()
        if not instance:
            instance = model.GoodPackage.objects.filter(bar_id=bar_id).first()
            if not instance:
                return JsonError("商品不存在，是否创建商品")
            package_number = instance.number
            buy_price = instance.one_package.buy_price * package_number
        else:
            package_number = 1
            buy_price = instance.buy_price
        data = {
            "id": instance.id,
            "bar_id": bar_id,
            "name": instance.name,
            "quantify": instance.quantify.name if instance.quantify else "-",
            "package_number": package_number,
            "buy_price": buy_price,
            "number": 1
        }
        return JsonSuccess("获取商品成功", data=data)

