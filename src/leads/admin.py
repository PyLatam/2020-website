from django.contrib import admin
from django.utils.html import format_html

from .models import LeadCode, LeadGroup


@admin.register(LeadCode)
class LeadCodeAdmin(admin.ModelAdmin):
    fields = ['account', 'code_image_display']
    readonly_fields = fields

    def code_image_display(self, obj):
        if not obj.code_image:
            return ''
        return format_html('<img src="{url}" />', url=obj.code_image.url)


@admin.register(LeadGroup)
class LeadGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
