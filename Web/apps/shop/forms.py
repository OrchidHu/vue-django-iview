from django import forms
from Web.apps.shop.models import Good

class CreateGoodForm(forms.ModelForm):

    class Meta:
        model = Good
        fields = (
            'bar_id',
            'name',
            'genre',
            'buy_price',
            'sale_price',
            'supplier'
        )
        error_messages = {
            "bar_id": {
                "max_length": u"输入正确的手机号码",
            },
        }