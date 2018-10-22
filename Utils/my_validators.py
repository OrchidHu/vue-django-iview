import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from Utils.my_regex import RE_IDENTIFI

@deconstructible
class UserIDCardValidator(validators.RegexValidator):
    regex = RE_IDENTIFI
    message = _(
        '请输入18位有效身份证号码'
    )
    flags = 0