from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Supplier(models.Model):
    """供货商"""

    name = models.CharField(
        max_length=50,
        verbose_name='名称'
    )
    describe = models.TextField(
        verbose_name='描述'
    )
    phone1 = models.CharField(
        max_length=20,
        verbose_name='电话'
    )
    phone2 = models.CharField(
        max_length=20,
        verbose_name='备用电话'
    )
    address = models.CharField(
        max_length=200,
        verbose_name='地址'
    )
    class Meta:
        verbose_name = _('供应商')
        verbose_name_plural = _('供应商')


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Quantify(models.Model):
    """计量单位"""
    name = models.CharField(
        max_length=30,
        verbose_name=u'单位',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name = '单位'
        verbose_name_plural = '单位'

    @property
    def get_name(self):
        return self.name

