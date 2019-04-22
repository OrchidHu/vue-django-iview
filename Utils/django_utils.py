# -*- coding: UTF-8 -*-
import datetime
import os, json
import time
import uuid
from Utils.db_connections import get_redis
from urllib import parse as _urlparse
from django.http import JsonResponse
from Conf import config
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


redis_db = get_redis()


def get_token():
    return uuid.uuid1()


def redis_get(key):
    ret = redis_db.get(key)
    if ret:
        return bytes.decode(ret, encoding="utf8")
    return ""


def get_genre_parent_id(child_data):
    if not child_data:
        return []
    ret = [str(child_data.id)]
    while child_data.parent:
        ret.append(str(child_data.parent_id))
        child_data = child_data.parent
    return ret[::-1]


def genre_display(query_data):
    display_list = []
    for genre in query_data:
        parent_dist = {
            'value': str(genre.id),
            'label': genre.title
        }
        display_list.append(parent_dist)
        children = genre.children.all()
        if len(children) > 0:
            parent_dist['children'] = genre_display(children)
    return display_list


def parse_put(request):
    payload = request.read()
    return dict(_urlparse.parse_qsl(payload))


def _fixfloat(num, fix_num=2):
    # 格式化浮点
    if not num:
        return 0
    num_str = repr(num).rstrip("0").rstrip(".")
    part_num = num_str.split('.')
    ret = part_num[0]
    if len(part_num) > 1:
        ret = ".".join((ret, part_num[1][:fix_num]))
    return ret or "0"


def str1datetime(time_str):
    if not time_str:
        return ''
    return datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)


def str2datetime(time_str, format=None):
    default_formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m',
        '%Y',
        '%Y/%m/%d',
        '%Y/%m',
        '%Y.%m',
    ]

    if format:
        default_formats.append(format)

    for format in default_formats[::-1]:
        try:
            time = datetime.datetime.strptime(time_str, format)
            return time
        except ValueError:
            continue
    return None


def batch_number():
    percent_time = time.strftime('%y%m%d%H', time.localtime(time.time()))
    uuid_number = str(int(uuid.uuid1()))[30:-1]
    return percent_time + uuid_number


def safe_compute(price, number, buy_price):
    if number > 0 and price > 0:
        return round(price/number, 2)
    else:
        return buy_price


def notice_manager(room_name, text_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            "type": "chat.message",
            "text": text_data
        }
    )


def JsonError(msg='', **kwargs):
    """ msg: 反馈给用户的信息
    kwargs: 会直接作为Json数据返回
    """

    ret = {
        'stat': 'error',
        'msg': msg
    }
    ret.update(kwargs)
    return JsonResponse(ret)


def JsonReLogin(msg='', **kwargs):

    ret = {
        'stat': 'error',
        'msg': msg,
        'relogin': 'true'
    }
    ret.update(kwargs)
    return JsonResponse(ret)


def JsonForbid(msg='', **kwargs):

    ret = {
        'stat': 'error',
        'msg': msg,
        'forbid': 'true'
    }
    ret.update(kwargs)
    return JsonResponse(ret)


def JsonSuccess(msg='', **kwargs):
    """ msg: 反馈给用户的信息
    kwargs: 会直接作为Json数据返回
    """
    ret = {
        'stat': 'success',
        'msg': msg
    }
    ret.update(kwargs)
    return JsonResponse(ret)


class ArgsMixin(object):

    def dispatch(self, *args, **kwargs):
        request = self.request
        user = request.user
        method = request.method
        method_args_map = {
            'GET': request.GET,
            'POST': json.loads(request.body) if request.body else '',
            'DELETE': request.GET,
        }
        self.args = method_args_map[method]
        return super(ArgsMixin, self).dispatch(*args, **kwargs)

    def get_arg(self, arg_key):
        return self.args.get(arg_key, '')

    def _dispatch_injection(self, *args, **kwargs):
        """ 执行method方法前的注入点，返回任何非空值将导致dispatch直接返回"""
        return

    def _list_ret(self, request, format_float=True):
        query_set = self._query_set()
        page = int(self.get_arg("page") or 1)
        page_size = config.PAGE_SIZE
        total_count = query_set.count()
        total_page = total_count / page_size
        if (total_count % page_size):
            total_page += 1
        datas = query_set[((page - 1) * page_size):(page * page_size)]
        ret = {
            "datas": self._parse_datas(datas),
            "page": page,
            "total_page": total_page,
        }
        if format_float:
            # 浮点固定两位小数返回
            for data_dict in ret["datas"]:
                if not isinstance(data_dict, dict):
                    continue
                for key, value in data_dict.iteritems():
                    if isinstance(value, float):
                        data_dict[key] = _fixfloat(value)
        return ret

    def get_instance(self, _id, model):
        try:
            return model.objects.get(id=_id)
        except Exception:
            return None

    def _invalid(self):
        return JsonError(u"无效的数据", reload=1)