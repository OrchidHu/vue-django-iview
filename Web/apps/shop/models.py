from django.utils.translation import ugettext_lazy as _
from django.db import models

class Good(models.Model):
    """商品资料"""

    bar_id = models.CharField(
        max_length=100,
        verbose_name=u'条码',
        unique=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name=u'名称'
    )
    genre= models.CharField(
        max_length=100,
        verbose_name=u"类别"
    )
    buy_price = models.FloatField(
        verbose_name=u"进货价"
    )
    sale_price = models.FloatField(
        verbose_name=u"销售价"
    )
    supplier = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=u"供货商"
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
