
# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from Web.apps.common.models import Quantify, Supplier
from Web.apps.shop.models import Good
from Web.models import XYUser
from django.contrib.auth.admin import UserAdmin

@admin.register(XYUser)
class XYUserAdmin(UserAdmin):
    # fieldsets为在admin后台可编辑对象的字段
    # 由于UserAdmin里定义了password隐藏的属性，因此我们继承它
    # 由于UserAdmin中的fieldsets中没有我们新定制的字段，所以这里我们重写fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'id_number',
                                         'gender', 'phone','email', 'avatar', 'position')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    # list_display 为在admin后台可显示对象的字段
    # display_name 是XYUser中自定义要显示的字段，可以设置显示颜色等
    list_display = ('username', 'email', 'display_name', 'phone',
                    'is_active', 'is_staff', 'is_superuser')
    search_fields = ['username','email','phone']
    list_filter = ['username']
    date_hierarchy = 'date_joined'

# 为新增加的Good添加显示字段
@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('bar_id', 'name', 'genre', 'quantify', 'buy_price', 'sale_price', 'supplier')
    list_display_links = ('bar_id', 'name', 'genre', 'quantify', 'buy_price', 'sale_price', 'supplier')
    search_fields = ['bar_id','name']
    list_filter = ['name']

admin.site.site_header = '鑫意超市后台管理系统'

# django1.7后新增了@admin.register装饰器向admin注册，这里废弃使用原有注册方式 admin.site.register()
# admin.site.register(XYUser, XYUserAdmin)
admin.site.register(Quantify)
admin.site.register(Supplier)