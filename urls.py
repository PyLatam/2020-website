# -*- coding: utf-8 -*-
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path


urlpatterns = [
    path('sitemap.xml', sitemap,
         {'sitemaps': {'flatpages': FlatPageSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path(r'', flatpage, {'url': '/'}, name='home'),
    path('<path:url>', flatpage),
    prefix_default_language=False,
)
