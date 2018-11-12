from django import forms
from Web.apps.shop.models import Good

class CreateGoodForm(forms.ModelForm):

    def clean_bar_id(self):
        bar_id = self.cleaned_data['bar_id']
        try:
            int(bar_id)
        except ValueError:
            raise forms.ValidationError("请输入正确的条码")
        return bar_id
    def clean(self):
        buy_price = self.cleaned_data['buy_price']
        sale_price = self.cleaned_data['sale_price']
        if sale_price < buy_price:
            raise forms.ValidationError("售价不能小于进价")
        return self.cleaned_data

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
                "max_length": u"条码过长",
                "required": u"条码是必填项"
            },
            "name": {
                "max_length": u"名称过长",
                "required": u"名称是必填项"
            },
            "genre": {
                "max_length": u"类别名过长",
                "required": u"类别是必填项"
            },
            "buy_price": {
                "required": u"进价是必填项"
            },
            "sale_price": {
                "required": u"售价是必填项"
            },
            "supplier": {
                "max_length": u"供应商名称过长",
                "required": u"供应商是必填项"
            }
        }