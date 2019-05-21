# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class JobAdsApp(CMSApp):
    name = _("Job ads")

    def get_urls(self, page=None, language=None, **kwargs):
        return ['job_ads.urls']


apphook_pool.register(JobAdsApp)
