#!/usr/bin/python
#coding=utf-8
import os

from Web.apps.common.models import Quantify, Supplier
from Web.apps.shop.models import Shop
from Web.models import XYUser
# import django
# django.setup()
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Web.settings'


def init_user():
    super_store = Shop.objects.create(
        name='总部'
    )
    XYUser.objects.create_superuser(
        username='admin',
        shop_id=super_store.id,
        meail='12345@qq.com',
        password='826446178lxl'
    )


def init_quantify():
    name_list = ['个', '包', '瓶', '袋', '支', '箱']
    for name in name_list:
        Quantify.objects.create(
            name=name
        )


def init_sulipper():
    Supplier.objects.create(
        name='临时供应商'
    )


if __name__ == '__main__':
    init_user()
    init_sulipper()
    init_quantify()
