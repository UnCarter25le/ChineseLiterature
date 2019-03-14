
from django import template

register = template.Library()

@register.filter

def makeList(strlist):
    
    str2list = [lists.replace('[','').replace(']','') for lists in strlist.split(',')]
    
    return str2list
# 使用過濾器時，不能有空格  ：showdata.3|makeList
