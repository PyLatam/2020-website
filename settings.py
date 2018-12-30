# -*- coding: utf-8 -*-

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

# all django settings can be altered here
ENABLE_SYNCING = False
STATIC_ROOT = '/static'
INSTALLED_APPS.extend([
    # add your project specific apps here
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'flatpages_extended',
])
