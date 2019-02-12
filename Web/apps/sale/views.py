# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View

from Utils.django_utils import JsonSuccess, ArgsMixin, JsonError, batch_number, str1datetime
from Utils.mixin_utils import XYUserRequiredMixin
from Web.apps.sale.forms import GoodOperateRecordForm
from Web.apps.sale.models import GoodOrder, GoodOperateRecord
from Web.apps.shop.models import GoodStock, Good


class GoodsSale(ArgsMixin, View):
    """商品出售"""

    def __init__(self):
        self.shop_id = -1

    def post(self, request):
        user = request.user
        if not user.shop:
            return JsonError("无对应门店数据")
        self.shop_id = user.shop.id
        goods_data = self.get_arg('goods_data')
        order_data = self.get_arg('order_data')
        serial_number = 'XY' + batch_number()
        buy_price_total = 0
        for data in goods_data:
            stock_instance = GoodStock.objects.filter(good_id=data['good_id'], shop_id=self.shop_id).first()
            good_instance = Good.objects.filter(id=data['good_id']).first()
            if not good_instance:
                return JsonError("无效数据")
            if not stock_instance:
                stock_instance = self.pre_sale(data, good_instance)
            stock_instance.number = stock_instance.number - data['number'] * data['package_number']
            stock_instance.save()
            buy_price_total += stock_instance.stock_buy_price * data['number']
            form = GoodOperateRecordForm(data)
            one_profit = data['sale_price'] - stock_instance.stock_buy_price
            profit = one_profit * data['number']
            if form.is_valid():
                instance = form.save(commit=False)
                instance.serial_number = serial_number
                instance.good_id = data['good_id']
                instance.quantify = good_instance.quantify or '-'
                instance.stock_buy_price = stock_instance.stock_buy_price
                instance.profit = profit
                instance.discount_profit = round(one_profit / data['sale_price'] * 100, 2)
                instance.operator = user
                instance.shop = user.shop
                instance.save()
        print(order_data)
        discount_profit = round((order_data['discMoney'] - buy_price_total) / order_data['discMoney'] * 100, 2)
        GoodOrder.objects.create(
            serial_number=serial_number,
            number=order_data['totalNumber'],
            buy_price_total=round(buy_price_total, 2),
            pre_sale_price=order_data['sumMoney'],
            discount_price=order_data['discMoney'],
            discount=order_data['discount'],
            profit=round(order_data['discMoney'] - buy_price_total, 2),
            discount_profit=discount_profit,
            operator=user,
            shop=user.shop
        )
        return JsonSuccess("结算成功")

    def pre_sale(self, data, good_instance):
        return GoodStock.objects.create(
            good_id=data['good_id'],
            shop_id=self.shop_id,
            number=0,
            stock_buy_price=good_instance.buy_price
        )

    def get(self, request):
        pass


class OrderList(ArgsMixin, View):
    """订单列表"""

    def post(self, request):
        user = request.user
        ret = []
        shop_id = self.get_arg('shop_id')
        operator_id = self.get_arg('person_id')
        start_time = str1datetime(self.get_arg('start_time'))
        end_time = str1datetime(self.get_arg('end_time'))
        query_kwargs = {}
        if not start_time or not end_time or not shop_id or not operator_id:
            return JsonError("请正确输入")
        query_kwargs['create_time__range'] = [start_time, end_time]
        if shop_id[0] != -1:
            query_kwargs['shop_id'] = shop_id[0]
        if operator_id[0] != -1:
            query_kwargs['operator_id'] = operator_id[0]
        query_set = GoodOrder.objects.filter(**query_kwargs)
        format = '%m-%d %H:%M:%S' if start_time and end_time and (end_time - start_time).days > 0 else '%H:%M:%S'
        for data in query_set:
            ret.append({
                'serial_number': data.serial_number,
                'operate_type': data.operate_type,
                'number': data.number,
                'text': self.format_text(data.serial_number),
                'discount_price': data.discount_price,
                'operator': data.operator.username,
                'create_time': data.create_time.strftime(format),
                'detail_create_time': data.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonSuccess("成功", data=ret)

    def format_text(self, serial_number):
        query_set = GoodOperateRecord.objects.filter(serial_number=serial_number).all()
        ret = ""
        for item in query_set:
            if ret:
                ret += "/"
            ret += item.name
        return ret


class OrderDetail(ArgsMixin, View):
    """订单详情"""

    def get(self, request):
        serial_number = self.get_arg('data')
        query_set = GoodOperateRecord.objects.filter(serial_number=serial_number).all()
        ret = []
        for item in query_set:
            ret.append({
                'serial_number': item.serial_number,
                'good_id': item.good.id,
                'bar_id': item.bar_id,
                'name': item.name,
                'quantify': item.quantify,
                'number': item.number,
                'sale_price': round(item.sale_price*item.number, 2),
                'operate_type': item.operate_type,
                'sale_status': item.sale_status,
                'operate_name': item.operator.username,
                'shop_name': item.shop.name,
                'create_time': item.create_time
            })
        return JsonSuccess("成功", data=ret)


class MarketingAnalysis(View):
    """销售分析"""

    def get(self, request):
        user = request.user
        fast_report = request.GET.get('fast_report')
        query_kwargs = {}
        if not user:
            return
        if fast_report:
            import datetime
            # 获取当前时间
            now = datetime.datetime.now()
            # 获取今天零点
            zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
            # 获取23:59:59
            lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
            query_kwargs['shop_id'] = user.shop
            query_kwargs['create_time__range'] = [zeroToday, lastToday]
        query_set = GoodOrder.objects.filter(
            operate_type='sale',
            sale_status='finish',
            **query_kwargs
        ).all()
        total_sale = 0
        total_profit = 0
        sales_favour = 0
        for data in query_set:
            total_sale += data.discount_price
            total_profit += data.profit
            sales_favour += data.pre_sale_price - data.discount_price
        data = {
            'total_sale': total_sale,
            'total_profit': total_profit,
            'sales_discount': total_profit/total_sale*100 if total_profit > 0 else 0,
            'sales_favour': sales_favour
        }
        return JsonSuccess("success", data=data)
