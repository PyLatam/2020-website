# -*- coding: utf-8 -*-
from getenv import env

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-django',
    'aldryn-django-cms',
    'djangocms-bootstrap4',
    'djangocms-file',
    'djangocms-link',
    'djangocms-picture',
    'djangocms-snippet',
    'djangocms-style',
    'djangocms-text-ckeditor',
    'djangocms-transfer',
    'django-filer',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

USE_TZ = True
USE_L10N = True
TIME_ZONE = 'America/Mexico_City'

CMS_TEMPLATES = (
    ('home.html', 'Home'),
    ('category.html', 'Category'),
    ('category_iframe.html', 'iFrame'),
    ('index_iframe_template.html', 'resumen_template'),
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
    # Third party
    'account',
    'account_extensions',
    'core',
    'leads',
    'schedule',
    'sponsors',
])

DJANGOCMS_FILE_TEMPLATES = [
    ('button', 'With button'),
]

MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.locale.LocaleMiddleware') + 1,
    'cms_extensions.middleware.LanguageCookieMiddleware',
)
MIDDLEWARE.remove('cms.middleware.language.LanguageCookieMiddleware')

# Captcha
if env('RECAPTCHA_PUBLIC_KEY') and env('RECAPTCHA_PRIVATE_KEY'):
    RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
else:
    # Use the test keys and be quiet about it
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Accounts
LOGIN_URL = 'account_login'
DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_LANGUAGES = (('es', 'Spanish'), ('en', 'English'))
ACCOUNT_OPEN_SIGNUP = env('ACCOUNT_OPEN_SIGNUP', default=True)
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_LOGIN_REDIRECT_URL = 'account_dashboard'
ACCOUNT_SETTINGS_REDIRECT_URL = 'account_settings'
ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL = 'account_dashboard'
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_AUTO_LOGIN = False
ACCOUNT_USER_DISPLAY = lambda user: user.email
AUTHENTICATION_BACKENDS.append('account.auth_backends.EmailAuthenticationBackend')


def ACCOUNT_DELETION_MARK_CALLBACK(account_deletion):
    # Fixes https://github.com/pinax/django-user-accounts/issues/241
    from account.hooks import hookset
    hookset.account_delete_expunge(account_deletion)

# Email
DEFAULT_FROM_EMAIL = 'PyLatam noreply@pylatam.org'

# Reservations
HOTEL_RESERVATIONS_URLS = {
    'es': 'https://secure.internetpower.com.mx/portals/Friendly/hotel/hoteldescription.aspx',
    'en': 'https://secure.internetpower.com.mx/portals/FriendlyEng/hotel/hoteldescription.aspx',
}

TALK_LANGUAGES = (
    ('en', 'English'),
    ('es', 'Español'),
)
