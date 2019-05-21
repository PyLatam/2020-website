# -*- coding: utf-8 -*-
from django.urls import path

from .views import JobAdListView


urlpatterns = [
    path('', JobAdListView.as_view(), name='job_ad_list'),
]
