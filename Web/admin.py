# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from Web.apps.common.models import Quantify, Supplier, Genre
from Web.apps.shop.models import Good, GoodPackage, Shop, GoodStock, StockRecord, ExamineStockRecord
from Web.models import XYUser
from django.contrib.auth.admin import UserAdmin


@admin.register(XYUser)
class XYUserAdmin(UserAdmin):
    # fieldsets为在admin后台可编辑对象的字段
    # 由于UserAdmin里定义了password隐藏的属性，因此我们继承它
    # 由于UserAdmin中的fieldsets中没有我们新定制的字段，所以这里我们重写fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'id_number',
                                         'shop', 'gender', 'phone', 'avatar', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    # list_display 为在admin后台可显示对象的字段
    # display_name 是XYUser中自定义要显示的字段，可以设置显示颜色等
    list_display = ('username', 'email', 'display_name', 'phone', 'shop',
                    'is_active', 'is_staff', 'is_superuser')
    search_fields = ['username', 'email', 'phone']
    list_filter = ['username']
    date_hierarchy = 'date_joined'


# 为新增加的Good添加显示字段


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('bar_id', 'name', 'genre', 'quantify', 'buy_price', 'sale_price', 'supplier')
    list_display_links = ('bar_id', 'name', 'genre', 'quantify', 'buy_price', 'sale_price', 'supplier')
    search_fields = ['bar_id', 'name']
    list_filter = ['name']


@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'stock_genre','bar_id', 'name', 'quantify', 'number', 'package_number',
                    'buy_price', 'shop_name', 'operator', 'create_time')
    search_fields = ['batch_number', 'bar_id', 'operator', 'name']
    list_filter = ['batch_number']

    def shop_name(self, obj):
        shop = Shop.objects.filter(id=obj.shop_id).first()
        return format_html(
            '<span style="color: #2d8cf0;">{}</span>',
            shop.name if shop else "-"
        )
    shop_name.short_description = u"所属门店"


admin.site.site_header = '鑫意超市后台管理系统'
admin.site.register(Quantify)


# django1.7后新增了@admin.register装饰器向admin注册，这里废弃使用原有注册方式 admin.site.register()
# admin.site.register(XYUser, XYUserAdmin)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'display_level')


@admin.register(GoodPackage)
class GoodPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'bar_id', 'quantify', 'number', 'sale_price')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'describe', 'phone1', 'phone2', 'address')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager', 'phone', 'create_time')


@admin.register(GoodStock)
class GoodStockAdmin(admin.ModelAdmin):
    list_display = ('good', 'shop', 'number', 'stock_buy_price', 'stock_sale_price')


@admin.register(ExamineStockRecord)
class ExamineStockRecordAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'total_price', 'shop_name', 'stock_genre', 'operator', 'examine_status_display', 'examine_person', 'examine_time',
                    'stock_status_display', 'stock_time')

    def examine_status_display(self, obj):
        if obj.examine_status == -1:
            return format_html(
                '<span>待审核</span>',
                obj.examine_status
            )
        if obj.examine_status == 0:
            return format_html(
                '<span style="color: red;">未通过</span>',
                obj.examine_status
            )
        if obj.examine_status == 1:
            return format_html(
                '<span style="color: green;">已通过</span>',
                obj.examine_status
            )

    def stock_status_display(self, obj):
        if obj.stock_status == 0:
            return format_html(
                '<span>未出入库</span>',
                obj.stock_status
            )
        if obj.stock_status == 1:
            return format_html(
                '<span style="color: green;">已出入库</span>',
                obj.stock_status
            )

    def shop_name(self, obj):
        shop = Shop.objects.filter(id=obj.shop_id).first()
        return format_html(
            '<span style="color: #2d8cf0;">{}</span>',
            shop.name if shop else "-"
        )

    shop_name.short_description = u"所属门店"
    examine_status_display.short_description = u"审核状态"
    stock_status_display.short_description = u"出入库状态"
