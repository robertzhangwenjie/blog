#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2018/12/22 21:13
# @Author   :   robert
# @FileName :   urls.py
# @Software :   PyCharm

from django.conf.urls import url

from my_blog.views import *
urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^archive/$',archive,name='archive'),
    url(r'^article/$',article,name='article'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'^logout$', do_logout, name='logout'),
    url(r'^reg', do_reg, name='reg'),
    url(r'^login', do_login, name='login'),
    url(r'^category/$', category, name='category'),
]
