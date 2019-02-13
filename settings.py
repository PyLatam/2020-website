# -*- coding: utf-8 -*-

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-django-cms',
    'djangocms-bootstrap4',
    'djangocms-picture',
    'djangocms-style',
    'djangocms-text-ckeditor',
    'djangocms-transfer',
    'django-filer',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

CMS_TEMPLATES = (
    ('home.html', 'Home'),
    ('category.html', 'Category'),
)
CMS_LANGUAGES = {
    'default': {
        'fallbacks': ['es', 'en'],
        'redirect_on_fallback': False,
        'public': True,
        'hide_untranslated': True,
    },
    1: [
        {'code': 'es', 'name': 'Spanish', 'fallbacks': [], 'public': True},
        {'code': 'en', 'name': 'English', 'fallbacks': [], 'public': True},
    ]
}
CMS_PAGE_CACHE = True

# all django settings can be altered here
ENABLE_SYNCING = False
STATIC_ROOT = '/static'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
INSTALLED_APPS.extend([
    # add your project specific apps here
    'django.contrib.flatpages',
    'flatpages_extended',
    'account',
])

MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.locale.LocaleMiddleware') + 1,
    'cms_extensions.middleware.LanguageCookieMiddleware',
)
MIDDLEWARE.remove('cms.middleware.language.LanguageCookieMiddleware')
