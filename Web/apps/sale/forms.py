from django import forms

from Web.apps.sale.models import GoodOperateRecord


class GoodOperateRecordForm(forms.ModelForm):

    class Meta:
        model = GoodOperateRecord
        fields = (
            'bar_id',
            'name',
            'quantify',
            'number',
            'package_number',
            'sale_price'
        )