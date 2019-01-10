# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.db import models


class Good(models.Model):
    """商品资料"""

    bar_id = models.CharField(
        max_length=30,
        verbose_name=u'条码',
        unique=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name=u'名称'
    )
    genre = models.ForeignKey(
        'common.Genre',
        verbose_name=u"类别",
        related_name="genre_goods",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    quantify = models.ForeignKey(
        'common.Quantify',
        verbose_name=u'单位',
        related_name="quantify_goods",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    buy_price = models.FloatField(
        verbose_name=u"进货价"
    )
    sale_price = models.FloatField(
        verbose_name=u"销售价"
    )
    supplier = models.ForeignKey(
        'common.Supplier',
        on_delete=models.PROTECT, # 设为删除保护
        related_name="supplier_shops",
        verbose_name=u"供货商",
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'shop_good'
        ordering = ['-id']
        verbose_name = _('商品')
        verbose_name_plural = _('商品')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    @property
    def get_name(self):
        return self.name

    @property
    def quantify_name(self):
        if self.quantify:
            return self.quantify.name
        else:
            return '-'


class GoodPackage(models.Model):
    """商品其他包装"""

    bar_id = models.CharField(
        max_length=30,
        verbose_name=u'包装条码',
        unique=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name=u'包装名称',
        unique=True
    )
    quantify = models.ForeignKey(
        'common.Quantify',
        verbose_name=u"包装单位",
        related_name="quantify_packages",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    one_package = models.ForeignKey(
        Good,
        on_delete=models.CASCADE,
        related_name="other_packages",
        verbose_name=u"单个包装"
    )
    package_number = models.IntegerField(
        verbose_name='包装数量'
    )
    sale_price = models.FloatField(
        verbose_name='包装售价'
    )

    @property
    def good_id(self):
        return self.one_package.id

    @property
    def quantify_name(self):
        if self.quantify:
            return self.quantify.name
        else:
            return '-'

    class Meta:
        ordering = ['-id']
        verbose_name = _('其他包装')
        verbose_name_plural = _('商品多包装')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Shop(models.Model):
    """门店"""
    name = models.CharField(
        max_length=200,
        verbose_name=u'门店名称',
        unique=True
    )
    address = models.CharField(
        max_length=200,
        verbose_name=u'门店地址',
        null=True,
        blank=True
    )
    manager = models.ForeignKey(
        'Web.XYUser',
        on_delete=models.CASCADE,
        related_name="set_shops",
        verbose_name=u"门店负责人",
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=50,
        verbose_name=u'门店电话',
        null=True,
        blank=True
    )
    create_time = models.DateTimeField(
        u'创建时间',
        auto_now_add=True,
        db_index=True,
    )

    @property
    def manager_phone(self):
        manager = self.manager
        if manager:
            return manager.phone
        return None

    class Meta:
        ordering = ['-id']
        verbose_name = _('门店')
        verbose_name_plural = _('门店')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class GoodStock(models.Model):
    """商品库存"""

    good = models.ForeignKey(
        Good,
        on_delete=models.CASCADE,
        related_name="set_stocks",
        verbose_name=u"商品",
        db_index=True
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.PROTECT,  # 设为删除保护
        related_name="set_stock_goods",
        verbose_name=u"所属门店"
    )
    number = models.IntegerField(
        verbose_name='门店库存'
    )
    stock_buy_price = models.FloatField(
        verbose_name='门店进价'
    )
    stock_sale_price = models.FloatField(
        verbose_name='门店售价',
        blank=True,
        null=True
    )

    @property
    def good_buy_price(self):
        return self.good.buy_price

    @property
    def good_quantify(self):
        return self.good.quantify_name

    class Meta:
        ordering = ['-id']
        verbose_name = _('商品库存')
        verbose_name_plural = _('商品库存')

    def __unicode__(self):
        return self.good.name

    def __str__(self):
        return self.__unicode__()


class StockRecord(models.Model):
    """出/入库记录"""

    STOCK_GENRE = (
        (1, u"入库"),
        (2, u"出库")
    )
    batch_number = models.CharField(
        "批次号",
        max_length=30
    )
    stock_genre = models.IntegerField(
        "操作类型",
        choices=STOCK_GENRE,
        default=1
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
        verbose_name='包装绑定数量'
    )
    buy_price = models.FloatField(
        verbose_name='单价'
    )
    operator = models.CharField(
        max_length=30,
        verbose_name=u"操作人"
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.PROTECT,
        verbose_name='所属门店'
    )
    create_time = models.DateTimeField(
        u'操作时间',
        auto_now_add=True,
        db_index=True,
    )

    @property
    def good_name(self):
        if self.good:
            return self.good.name
        return '未知商品'

    @property
    def shop_name(self):
        if self.shop:
            return self.shop.name
        return '-'

    @property
    def total_number(self):
        return self.number * self.package_number

    class Meta:
        ordering = ['-id']
        verbose_name = _('出/入库记录')
        verbose_name_plural = _('出/入库记录')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class ExamineStockRecord(models.Model):
    """出入库审核"""

    EXAMINE_STATUS = (
        (-1, u"待审核"),
        (0, u"未通过"),
        (1, u"已通过")
    )
    STOCK_STATUS = (
        (0, u"未出/入库"),
        (1, u"已出/入库")
    )
    STOCK_GENRE = (
        (1, u"入库"),
        (2, u"出库")
    )
    batch_number = models.CharField(
        "批次号",
        max_length=30
    )
    total_price = models.FloatField(
        """总金额"""
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.PROTECT,
        verbose_name='所属门店'
    )
    stock_genre = models.IntegerField(
        "操作类型",
        choices=STOCK_GENRE,
        default=1
    )
    operator = models.CharField(
        max_length=30,
        verbose_name=u"操作人"
    )
    examine_status = models.IntegerField(
        "审核状态",
        choices=EXAMINE_STATUS,
        default=-1
    )
    examine_person = models.CharField(
        "审核人",
        max_length=30,
        default='-'
    )
    examine_time = models.DateTimeField(
        "审核日期",
        blank=True,
        null=True
    )
    stock_status = models.IntegerField(
        "出/入库状态",
        choices=STOCK_STATUS,
        default=0
    )
    stock_time = models.DateTimeField(
        "出/入库日期",
        blank=True,
        null=True
    )

    @property
    def shop_name(self):
        return self.shop.name if self.shop else '-'

    def __unicode__(self):
        return self.batch_number

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-id']
        verbose_name = _('审核记录')
        verbose_name_plural = _('审核记录')

