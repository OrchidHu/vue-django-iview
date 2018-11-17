from django.shortcuts import render

# Create your views here.
from django.views.generic import View
import Web.apps.common.models as model
from Utils.django_utils import JsonSuccess, JsonError


class QuantifyList(View):
    """单位列表"""

    def get(self, request):
        query_data =  model.Quantify.objects.all()
        if query_data:
            ret = []
            for em in query_data:
                ret.append({
                    'value': em.id,
                    'label': em.name
                })
            return JsonSuccess("请求成功", data=ret)
        return JsonError('没有权限')


class SupplierList(View):
    """供应商"""

    def get(self, request):
        query_data =  model.Supplier.objects.all()
        if query_data:
            ret = []
            for em in query_data:
                ret.append({
                    'value': em.id,
                    'label': em.name
                })
            return JsonSuccess("请求成功", data=ret)
        return JsonError('没有权限')