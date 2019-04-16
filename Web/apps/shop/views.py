# -*- coding: UTF-8 -*-
import datetime
import json
import django.utils.timezone as timezone

from django.contrib.auth import logout
from django.db.models import Q
from django.views.generic import View

import Web.apps.shop.models as model
from Utils.db_connections import get_redis
from Utils.django_utils import JsonError, JsonSuccess, redis_get, JsonReLogin, \
    JsonForbid, get_genre_parent_id, batch_number, notice_manager, safe_compute
from Web.apps.shop.forms import CreateGoodForm, CreateOtherPackageForm, CreateStockRecordForm


class Good(View):

    def get(self, request):
        user = request.user
        token = request.COOKIES.get("token")
        db_token = redis_get(user.username)
        # if not db_token or db_token != token:
        #     logout(request)
        #     return JsonReLogin('需要身份验证')
        if user.is_staff:
            data = self.get_data()
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
        print(data)
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
            good.supplier_id = data.get('supplier_id')
            good.quantify_id = data.get('quantify_id')
            good.genre_id = data['genre_id'][-1] if data['genre_id'] else None
            good.save()
            return JsonSuccess("保存成功")
        return JsonError("提交数据有误")


class Delete(View):
    """删除商品"""

    def get(self, request):
        import time
        json_data = request.GET.get('data')
        data = json.loads(json_data)
        if data['del_list']:
            for good in data.get('del_list'):
                try:
                    model.Good.objects.filter(id=good['id']).delete()
                except Exception as e:
                    print([item .name for item in e.protected_objects])
                    notice_manager("sys", "你有审批任务啦")
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
                'package_number': data.number,
                'sale_price': data.sale_price
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
    if float(cost_price) > float(data['sale_price']):
        return False
    return True


class ScanStockSearch(View):
    """出入库扫码搜索"""

    def get(self, request):
        bar_id = request.GET.get('data')
        instance = model.Good.objects.filter(bar_id=bar_id).first()
        if not instance:
            instance = model.GoodPackage.objects.filter(bar_id=bar_id).first()
            if not instance:
                return JsonError("商品不存在，是否创建商品")
            package_number = instance.package_number
            buy_price = instance.one_package.buy_price * package_number
        else:
            package_number = 1
            buy_price = instance.buy_price
        data = {
            "good_id": instance.good_id if hasattr(instance, 'one_package') else instance.id,
            "bar_id": bar_id,
            "name": instance.name,
            "quantify": instance.quantify.name if instance.quantify else "-",
            "package_number": package_number,
            "buy_price": buy_price,
            "number": 1
        }
        return JsonSuccess("获取商品成功", data=data)


class ScanSaleSearch(View):
    """扫码出售搜索"""

    def get(self, request):
        bar_id = request.GET.get('data')
        instance = model.Good.objects.filter(bar_id=bar_id).first()
        if not instance:
            instance = model.GoodPackage.objects.filter(bar_id=bar_id).first()
            if not instance:
                return JsonError("商品不存在，是否创建商品")
            sale_price = instance.sale_price
            good_id = instance.good_id
            package_number = instance.package_number
        else:  # 单包装查询是否有门店售价
            good_id = instance.id
            pack_good = model.GoodStock.objects.filter(good_id=good_id).first()
            package_number = 1
            if pack_good and pack_good.stock_sale_price:
                sale_price = pack_good.stock_sale_price
            else:
                sale_price = instance.sale_price
        data = {
            'name': instance.name,
            'bar_id': bar_id,
            'good_id': good_id,
            'number': 1,
            'package_number': package_number,
            'sale_price': sale_price,
            'subtotal': sale_price
        }
        return JsonSuccess("查询成功", data=data)


class SearchGoodSale(View):
    """搜索出售商品"""

    def get(self, request):
        keyword = request.GET.get('data')
        if not keyword:
            return JsonError("keyword不能为空")
        good_sets = model.Good.objects.filter(Q(bar_id__contains=keyword) | Q(name__contains=keyword)).all()[:10]
        package_sets = model.GoodPackage.objects.filter(Q(bar_id__contains=keyword) | Q(name__contains=keyword)).all()[:10]
        if not good_sets and not package_sets:
            return JsonError("暂无结果")
        data = []
        for item in good_sets:
            data.append({
                'name': item.name,
                'bar_id': item.bar_id,
                'good_id': item.id,
                'package_number': 1,
                'sale_price': '%.2f' % item.sale_price,
                'quantify': item.quantify_name
            })
        for item in package_sets:
            data.append({
                'name': item.name,
                'bar_id': item.bar_id,
                'good_id': item.good_id,
                'package_number': item.package_number,
                'sale_price': '%.2f' % item.sale_price,
                'quantify': item.quantify_name
            })
        return JsonSuccess("查询成功", data=data[:8])


class GoodStockRecord(View):
    """"添加入库记录"""

    def post(self, request):
        try:
            json_data = request.body
            data = json.loads(json_data)
        except Exception:
            return JsonError("解析失败")
        record = data.get('list')
        if not record:
            return JsonError("无效数据")
        batch_num = batch_number()
        user = request.user
        # 权限判断
        if not user or not user.shop:
            return JsonError("没有入库权限")
        for item in record:
            form = CreateStockRecordForm(item)
            if form.is_valid():
                stock_record = form.save(commit=False)
                stock_record.batch_number = batch_num
                stock_record.operator = user.username
                stock_record.shop_id = user.shop.id
                stock_record.good_id = item.get('good_id')
                stock_record.save()
            else:
                print(form.errors)

        model.ExamineStockRecord.objects.create(
            batch_number=batch_num,
            total_price=data.get('total_price'),
            shop_id=user.shop.id,
            stock_genre=data.get('stock_genre') or 1,
            operator=user.username
        )
        notice_manager("sys_message", "你有审批任务啦")
        return JsonSuccess("入库提交成功")


class ExamTaskList(View):
    """审核任务列表"""

    def get(self, request):
        user = request.user
        if user:
            if user.has_perm('boss'):
                tasks = model.ExamineStockRecord.objects.filter(examine_status=-1)
            elif user.has_perm('manager'):
                tasks = model.ExamineStockRecord.objects.filter(examine_status=-1, shop=user.shop)
            else:
                return JsonError("无权操作")
            ret = []
            for task in tasks:
                result = {
                    'batch_number': task.batch_number,
                    'shop': task.shop_name,
                    'examine_status': task.examine_status,
                    'examine_display': task.get_examine_status_display(),
                    'stock_genre': task.get_stock_genre_display()
                }
                ret.append(result)
            return JsonSuccess("获取成功", data=ret)
        return JsonError("无权操作")


class CommitExamTask(View):
    """审批任务提交"""

    # def get(self, request):
    #     __import__("pdb").set_trace()
    #     try:
    #         json_data = request.GET.get('data')
    #         data = json.loads(json_data)
    #     except Exception:
    #         return JsonError("解析失败")
    #     if not data:
    #         return JsonError("无效数据")
    #     user = request.user
    #
    #     return JsonSuccess("")

    def get_data(self, batch_number):
        query_set = model.StockRecord.objects.filter(batch_number=batch_number)
        ret = []
        for data in query_set:
            ret.append({
                'bar_id': data.bar_id,
                'stock_genre': data.stock_genre,
                'good_name': data.good_name,
                'quantify': data.quantify,
                'number': data.number,
                'package_number': data.package_number,
                'buy_price': data.buy_price,
                'operator': data.operator,
                'shop_name': data.shop_name,
                'create_time': data.create_time.strftime("%Y-%m-%d %H:%S:%M")
            })
        return ret

    def post(self, request):
        try:
            json_data = request.body
            data = json.loads(json_data)
        except Exception:
            return JsonError("解析失败")
        if not data:
            return JsonError("无效数据")
        exam_batch = data
        user = request.user
        # 权限判断
        if not user or not user.shop:
            return JsonError("没有入库权限")
        examine_status = exam_batch['examine_status']
        if examine_status == -1:
            result = self.get_data(exam_batch['batch_number'])
            return JsonSuccess("", data=result)
        if examine_status == 1:
            self.update_stock_data(exam_batch)
        exam_query_set = model.ExamineStockRecord.objects.filter(batch_number=exam_batch['batch_number']).first()
        exam_query_set.examine_status = examine_status
        exam_query_set.examine_person = user.username
        exam_query_set.examine_time = timezone.now()
        exam_query_set.stock_status = 1 if examine_status else 0
        exam_query_set.stock_time = timezone.now()
        exam_query_set.save()
        return JsonSuccess("操作成功")

    @staticmethod
    def update_stock_data(exam_batch):
        query_set = model.StockRecord.objects.filter(batch_number=exam_batch['batch_number'])
        for data in query_set:
            good_stock = model.GoodStock.objects.filter(good_id=data.good_id, shop_id=data.shop_id).first()
            if not good_stock:
                model.GoodStock.objects.create(
                    good_id=data.good_id,
                    shop_id=data.shop_id,
                    number=data.number if data.stock_genre == 1 else (0 - data.number),
                    stock_buy_price=data.buy_price
                )
            else:
                stock_total_price = good_stock.number * good_stock.stock_buy_price
                record_total_price = data.number * data.buy_price
                # 如果是入库记录
                if data.stock_genre == 1:
                    number = good_stock.number + data.total_number
                    total_price = stock_total_price + record_total_price
                    buy_price = safe_compute(total_price, number, data.good.buy_price)
                else:
                    number = good_stock.number - data.total_number
                    total_price = stock_total_price - record_total_price
                    buy_price = safe_compute(total_price, number, data.good.buy_price)
                good_stock.number = number
                good_stock.stock_buy_price = buy_price
                good_stock.save()


class ShopList(View):
    """门店列表"""

    def get(self, request):
        user = request.user
        if not user.shop:
            return JsonError("没有绑定相关门店")
        user_data = {'value': user.shop.id, 'label': user.shop.name}
        if user.has_perm('Web.boss'):
            shops = model.Shop.objects.all()
            ret = [{'value': -1, 'label': '全部'}]
            for shop in shops:
                ret.append({
                    'value': shop.id,
                    'label': shop.name
                })
            result = {
                'shop_data': ret,
                'user_data': [user.shop.id],
                'identity': 'boos'
            }
            return JsonSuccess("门店列表", data=result)
        else:
            ret = {'shop_data': [user_data], 'user_data': [user.shop.id], 'identity': 'manager'}
            return JsonSuccess("门店列表", data=ret)


class SearchStockReport(View):
    """库存查询"""

    def post(self, request):
        try:
            json_data = request.body
            data = json.loads(json_data)
        except Exception:
            return JsonError("解析失败")
        if not data:
            return JsonError("无效数据")
        query_args = []
        query_kwargs = {}
        keyword = data.get('searchValue')
        current = data.get('currentPage')
        shop_id = data['shopSelected'].pop() if data['shopSelected'] else None
        genre_id = data['genreSelected'].pop() if data['genreSelected'] else None
        if keyword:
            query_args.append(
                Q(good__name__contains=keyword)|
                Q(good__bar_id__contains=keyword)
            )
        if shop_id != -1:
            query_kwargs['shop_id'] = shop_id
        if genre_id:
            query_kwargs['good__genre_id'] = genre_id
        query_set = model.GoodStock.objects.filter(
            *query_args, **query_kwargs
        )
        ret = []
        for data in query_set:
            ret.append({
                'good_name': data.good.name,
                'bar_id': data.good.bar_id,
                'shop_name': data.shop.name,
                'number': data.number,
                'quantify': data.good_quantify,
                'stock_buy_price': round(data.stock_buy_price, 2),
                'stock_sale_price': round(data.good.sale_price if not data.stock_sale_price else data.stock_sale_price, 2)
            })
        return JsonSuccess("", data=ret[(current-1)*15: current*15], total=len(ret))