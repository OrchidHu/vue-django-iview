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
        related_name="q_goods",
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
        related_name="to_shops",
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
