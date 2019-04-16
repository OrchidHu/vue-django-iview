#!/usr/bin/python
#coding=utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Web.settings'  # 此处要注意自己的项目路径
import django
django.setup()
from Web.apps.common.models import Quantify, Supplier
from Web.apps.shop.models import Shop
from Web.models import XYUser
# import django
# django.setup()
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Web.settings'


def init_user():

    super_store = Shop.objects.get_or_create(
        name='总部'
    )
    admin = XYUser.objects.filter(username='admin').first()
    if not admin:
        XYUser.objects.create_superuser(
            username='admin',
            shop_id=super_store.id,
            email='12345@qq.com',
            password='826446178lxl'
        )


def init_quantify():
    name_list = ['个', '包', '瓶', '袋', '支', '箱']
    for name in name_list:
        Quantify.objects.get_or_create(
            name=name
        )


def init_sulipper():
    Supplier.objects.get_or_create(
        name='临时供应商'
    )


if __name__ == '__main__':
    init_user()
    init_sulipper()
    init_quantify()
