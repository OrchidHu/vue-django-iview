# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Q

from Web.apps.common.models import Supplier, Quantify
from Web.apps.shop.models import Shop
from Web.models import XYUser


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            '-n',
            '--name',
            action='store',
            dest='name',
            default='close',
            help='name of author.',
        )

    def init_admin(self):
        shop = Shop.objects.filter(
            name='总部'
        ).first()
        if not shop:
            shop = Shop.objects.create(
                name='总部'
            )
        admin = XYUser.objects.filter(
            username='admin'
        ).first()
        if not admin:
            admin = XYUser.objects.create(
                username='admin',
                shop_id=shop.id,
                is_superuser=True,
                is_staff=True
            )
            admin.set_password('826446178lxl')
            admin.save()
        if not shop.manager:
            shop.manager = admin
            shop.save()

    def init_supplier(self):
        """初始化供应商"""
        supplier = Supplier.objects.filter(
            name='临时供应商'
        ).first()
        if not supplier:
            Supplier.objects.create(
                name='临时供应商'
            )

    def init_quantify(self):
        """初始化单位"""

        quantify_list = ['个', '包', '瓶', '支']
        for quan in quantify_list:
            quantify = Quantify.objects.filter(
                name=quan
            ).first()
            if not quantify:
                Quantify.objects.create(
                    name=quan
                )

    def handle(self, *args, **options):

        self.init_admin()
        self.init_supplier()
        self.init_quantify()
        try:
            if options['name']:
                print(
                'hello world, %s' % options['name'])

            self.stdout.write(self.style.SUCCESS('命令%s执行成功, 参数为%s' % (__file__, options['name'])))
        except Exception as ex:
            self.stdout.write(self.style.ERROR('命令执行出错'))