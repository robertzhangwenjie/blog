#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2018/12/23 21:10
# @Author   :   robert
# @FileName :   myfilter.py
# @Software :   PyCharm

from django import template
register = template.Library()

# 定义一个将日期中的月份转换为大写的过滤器，如1转换为一
@register.filter(name='month_to_upper')
def month_to_upper(key):
    return {
        '1':'一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九',
        '10': '十',
        '11': '十一',
        '12': '十二',
    }.get(str(key.month),None)

# @register.filter
# def month_to_upper(key):
#         return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][key.month-1]


if __name__ == '__main__':
    pass