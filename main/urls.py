# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^currency/converse$', views.currency_converse, name='currency_converse'),
]