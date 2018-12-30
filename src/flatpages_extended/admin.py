from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as BaseFlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site


class FlatPageAdmin(BaseFlatPageAdmin):
    fields = ('title', 'url', 'template_name')
    fieldsets = None
    list_display = ('title', 'url')
    list_filter = []
    search_fields = ('url', 'title')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.sites.add(Site.objects.get_current(request))


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
