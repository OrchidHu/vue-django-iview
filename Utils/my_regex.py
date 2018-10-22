#coding=utf-8
import re

RE_PHONE = re.compile(r'^(\d{5}|\d{3,4}(|-)\d{3,4}(|-)\d{3,4})$')
RE_MOBILE_PHONE = re.compile(r'^1[3|4|5|7|8]\d{9}$')
RE_IDENTIFI = re.compile(r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])(\d{3})(\d|x|X)$')
RE_EMAIL = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE  # domain
)
RE_NACTION = re.compile(u"(?<=nAction:)\d+")
RE_TRUCK_NUM = re.compile(u'^[\u4e00-\u9fa5][A-Za-z][A-Za-z0-9]{5}$')
