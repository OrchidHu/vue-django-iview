from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from Web.apps.shop.models import Good


class GoodOperateRecord(models.Model):
    """商品运营记录"""

    OPERATE_TYPE = (
        ('sale', '出售'),
        ('return', '退货'),
        ('damage', '报损')
    )
    ORDER_STATUS = (
        ('finish', '完成'),
        ('return', '退订')
    )
    serial_number = models.CharField(
        "流水号",
        max_length=100,
        db_index=True
    )
    good = models.ForeignKey(
        Good,
        on_delete=models.PROTECT,
        verbose_name='商品'
    )
    bar_id = models.CharField(
        max_length=30,
        verbose_name=u'条码'
    )
    name = models.CharField(
        max_length=200,
        verbose_name=u'名称'
    )
    quantify = models.CharField(
        max_length=30,
        verbose_name=u"单位",
        null=True,
        blank=True
    )
    number = models.IntegerField(
        verbose_name='数量'
    )
    package_number = models.IntegerField(
        verbose_name='包装数量'
    )
    stock_buy_price = models.FloatField(
        '成本价'
    )
    sale_price = models.FloatField(
        verbose_name='售价'
    )
    profit = models.FloatField(
        '毛利润'
    )
    discount_profit = models.FloatField(
        '毛利率'
    )
    operate_type = models.CharField(
        '操作类型',
        max_length=20,
        choices=OPERATE_TYPE,
        default='sale'
    )
    sale_status = models.CharField(
        '订单状态',
        max_length=20,
        choices=ORDER_STATUS,
        default='finish'
    )
    operator = models.ForeignKey(
        'Web.XYUser',
        on_delete=models.PROTECT,
        related_name="set_goods_sale",
        verbose_name=u"销售人"
    )
    shop = models.ForeignKey(
        'shop.Shop',
        on_delete=models.PROTECT,
        verbose_name='所属门店'
    )
    create_time = models.DateTimeField(
        u'操作时间',
        auto_now_add=True,
        db_index=True,
    )

    def operate_name(self):
        return self.operator.username if self.operator else '-'

    def shop_name(self):
        return self.shop.name if self.shop else '-'

    shop_name.short_description = u'门店'
    shop_name.short_description = u'操作人'

    def __unicode__(self):
        return self.serial_number

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-id']
        verbose_name = _('商品运营记录')
        verbose_name_plural = _('商品运营记录')


class GoodOrder(models.Model):
    """运营订单"""

    OPERATE_TYPE = (
        ('sale', '出售'),
        ('return', '退货'),
        ('damage', '报损')
    )
    ORDER_STATUS = (
        ('finish', '完成'),
        ('return', '退订'),
        ('credit', '挂单')
    )
    serial_number = models.CharField(
        "流水号",
        max_length=100,
        db_index=True
    )
    operate_type = models.CharField(
        '操作类型',
        max_length=20,
        choices=OPERATE_TYPE,
        default='sale'
    )
    sale_status = models.CharField(
        '订单状态',
        max_length=20,
        choices=ORDER_STATUS,
        default='finish'
    )
    number = models.IntegerField(
        "商品个数"
    )
    buy_price_total = models.FloatField(
        '成本总额'
    )
    pre_sale_price = models.FloatField(
        "预期售价总额"
    )
    discount_price = models.FloatField(
        "实际售价总额"
    )
    discount = models.FloatField(
        "折扣"
    )
    profit = models.FloatField(
        "毛利润"
    )
    discount_profit = models.FloatField(
        "毛利率"
    )
    operator = models.ForeignKey(
        'Web.XYUser',
        on_delete=models.PROTECT,
        related_name="set_orders",
        verbose_name=u"订单操作人"
    )
    shop = models.ForeignKey(
        'shop.Shop',
        on_delete=models.PROTECT,
        verbose_name='所属门店'
    )
    create_time = models.DateTimeField(
        u'创建时间',
        auto_now_add=True,
        db_index=True,
    )
    update_time = models.DateTimeField(
        "更新时间",
        blank=True,
        null=True
    )

    def operate_name(self):
        return self.operator.username if self.operator else '-'

    def shop_name(self):
        return self.shop.name if self.shop else '-'

    shop_name.short_description = u'门店'
    operate_name.short_description = u'操作人'

    def __unicode__(self):
        return self.serial_number

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-id']
        verbose_name = _('运营订单')
        verbose_name_plural = _('运营订单')

