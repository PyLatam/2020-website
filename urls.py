# -*- coding: utf-8 -*-
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from cms.sitemaps import CMSSitemap


urlpatterns = [
    path('sitemap.xml', sitemap,
         {'sitemaps': {'cmspages': CMSSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('cms.urls')),
    prefix_default_language=False,
)
