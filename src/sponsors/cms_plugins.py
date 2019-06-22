from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Sponsor, SponsorsListPlugin


class SponsorsList(CMSPluginBase):
    model = SponsorsListPlugin
    render_template = 'sponsors/cms_plugins/sponsors_list.html'

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['sponsors'] = Sponsor.objects.filter(
            is_active=True,
            level=instance.level,
        )
        return context


plugin_pool.register_plugin(SponsorsList)
