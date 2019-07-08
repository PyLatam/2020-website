from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ScheduleApp(CMSApp):
    name = 'Schedule'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['schedule.urls']


apphook_pool.register(ScheduleApp)
