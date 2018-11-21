from django.shortcuts import render

# Create your views here.
from django.views.generic import View
import Web.apps.common.models as model
from Utils.django_utils import JsonSuccess, JsonError, genre_display


def query_quantify():
    query_data =  model.Quantify.objects.all()
    ret = []
    for em in query_data:
        ret.append({
            'value': em.id,
            'label': em.name
        })
    return ret


class QuantifyList(View):
    """单位列表"""

    def get(self, request):
        data = query_quantify()
        return JsonSuccess("请求成功", data=data)


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


class GenreList(View):
    """分类列表"""

    def get(self, request):
        query_data =  model.Genre.objects.all()
        if query_data:
            parent_genre = []
            for em in query_data:
                if em.level == 0:
                    parent_genre.append(em)
            data = genre_display(parent_genre)
            return JsonSuccess("请求成功", data=data)
        return JsonError('没有数据')


class AddQuantify(View):
    """添加单位"""

    def get(self, request):
        quantify = request.GET.get('data')
        query_set = model.Quantify.objects.filter(name=quantify).first()
        if query_set:
            return JsonError('单位"%s"已存在' % query_set)
        new = model.Quantify.objects.create(name=quantify)
        ret = {
            'current_id': new.id,
            'quantify_list': query_quantify()
        }
        return JsonSuccess("添加成功", data=ret)
