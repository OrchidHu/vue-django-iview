from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from django.contrib.auth.models import (
    UserManager,
    Group, Permission, AbstractUser, User)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from Utils.my_validators import UserIDCardValidator


class Goods(models.Model):
    """商品资料"""

    bar_id = models.IntegerField(
            verbose_name=u'条码',
            db_index=True
    )
    name = models.CharField(
            max_length=200,
            verbose_name=u'名称'
    )
    genre= models.CharField(
            max_length=200,
            verbose_name=u"类别"
    )
    buy_price = models.IntegerField(
            verbose_name=u"进货价"
    )
    sale_price = models.IntegerField(
            verbose_name=u"销售价"
    )
    supplier = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=u"供货商"
    )


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


    @property
    def get_name(self):
        return self.name

class XYUser(models.Model):
    id_card_validator = UserIDCardValidator()

    POSITION = (
        ('boss', u'老板'),
        ('manager', u'管理员'),
        ('cashier', u'收银员'),
        ('waiter', u'服务员'),
        ('pullover', u"送货员")
          )
    SEX = (
        ('boy', u"男"),
        ('girl', u"女")
    )
    user = models.OneToOneField(
        User,
        related_name='xu_user',
        verbose_name=u'鑫意客户',
        on_delete=True,
        null=True,
        blank=True,
    )

    first_name = models.CharField(u'姓', max_length=30)
    last_name = models.CharField(u'名', max_length=30)
    sex = models.CharField(
        verbose_name=_('性别'),
        max_length=10,
        choices=SEX,
        default='boy',
    )
    email = models.EmailField(_('邮箱地址'), db_index=True, unique=True)
    phone = models.CharField(
        max_length=15,
        verbose_name=u'手机号码',
        db_index=True,
        null=True,
        blank=True,
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
        upload_to='driver/%Y/%m/%d'
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
    def __str__(self):
        if self.first_name or self.last_name:
            return "%s(%s)" % (self.user.username, self.first_name+self.last_name)
        return  "%s" % self.user.username

    class Meta:

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


