from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import (
    UserManager, AbstractUser)
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from Utils.my_validators import UserIDCardValidator, PhoneValidator


class XYUser(AbstractUser):
    id_card_validator = UserIDCardValidator()
    phone_validator = PhoneValidator()
    email_validator = EmailValidator()

    POSITION = (
        ('boss', u'老板'),
        ('manager', u'管理员'),
        ('cashier', u'收银员'),
        ('waiter', u'服务员'),
        ('pullover', u"送货员")
          )
    GENDER = (
        ('boy', u"男"),
        ('girl', u"女")
    )

    first_name = models.CharField(u'姓', max_length=30, validators=[MaxLengthValidator(30)])
    last_name = models.CharField(u'名', max_length=30, validators=[MaxLengthValidator(30)])
    gender = models.CharField(
        verbose_name=_('性别'),
        max_length=10,
        choices=GENDER,
        default='boy',
    )
    email = models.EmailField(
        _('邮箱地址'),
        max_length=50,
        db_index=True,
        unique=True,
        validators=[email_validator]
    )
    phone = models.CharField(
        max_length=15,
        verbose_name=u'手机号码',
        db_index=True,
        validators=[phone_validator]
    )
    id_number = models.CharField(
        max_length=80,
        help_text=_('请输入18位有效身份证号码'),
        validators=[id_card_validator],
        verbose_name=u'身份证号',
    )
    avatar = models.ImageField(
        u"头像",
        max_length=200,
        null=True,
        blank=True,
        upload_to='images/%Y/%m/%d'
    )
    position = models.CharField(
        verbose_name=_('职位'),
        max_length=30,
        choices=POSITION,
        default='cashier',
    )
    last_login = models.DateTimeField(_('最后一次登录'), blank=True, null=True)
    date_joined = models.DateTimeField(_('加入时间'), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # 返回此model实例对象名称，如在admin中xyuser可见

    class Meta:
        db_table = 'auth_user'
        ordering = ['-id']
        verbose_name = _('鑫意用户')
        verbose_name_plural = _('用户')
        permissions = (
            ('boos', u'老板'),
            ('manager', u'管理员'),
            ('cashier', u'收银员'),
            ('staff', u"普通员工"),
            ('goods_manage', u'商品管理'),
            ('sale_manage', u'销售管理'),
            ('order_goods_manage', u'进货管理'),
            ('stock_manage', u'库存管理'),
            ('report_manage', u'报表管理'),
            ('setting_manage',u'设置管理')
        )

    def display_name(self):
        return format_html(
            '<span style="color: #2d8cf0;">{} {}</span>',
            self.first_name,
            self.last_name,
        )
    display_name.short_description = u"姓 名"