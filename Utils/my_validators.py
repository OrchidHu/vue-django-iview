import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from Utils.my_regex import RE_IDENTIFI, RE_PHONE, RE_EMAIL


@deconstructible
class UserIDCardValidator(validators.RegexValidator):
    regex = RE_IDENTIFI
    message = _(
        '请输入18位有效身份证号码'
    )
    flags = 0

@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = RE_PHONE
    message = _(
        '请输入正确的手机号码'
    )
    flags = 0

# 继承的RegexValidator中已有全面的EmailValidator验证方法
@deconstructible
class EmailValidator(validators.RegexValidator):
    regex = RE_EMAIL
    message = _(
        '请输入正确的邮箱地址'
    )
    flags = 0