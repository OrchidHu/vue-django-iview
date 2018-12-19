from django.db import models
from django.utils.html import format_html
from mptt.models import MPTTModel
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Supplier(models.Model):
    """供货商"""

    name = models.CharField(
        max_length=50,
        verbose_name='名称'
    )
    describe = models.TextField(
        verbose_name='描述',
        blank=True,
        null=True
    )
    phone1 = models.CharField(
        max_length=20,
        verbose_name='电话',
        blank=True,
        null=True
    )
    phone2 = models.CharField(
        max_length=20,
        verbose_name='备用电话',
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=200,
        verbose_name='地址',
        blank=True,
        null=True
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
        unique=True,
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


class Genre(MPTTModel):
    title = models.CharField('名称', max_length=50, unique=True)
    parent = models.ForeignKey(
        'self',
        verbose_name='所属类别',
        null=True, blank=True,
        related_name='children',
        on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'common_genre'
        verbose_name = verbose_name_plural = '类别'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


    def display_level(self):
        return format_html(
            '<span>{}</span>',
            self.level
        )
    display_level.short_description = u"分类级别"