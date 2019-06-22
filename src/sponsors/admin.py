from django.contrib import admin

from .models import Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'position']
    fields = ['position', 'name', 'website', 'contact', 'logo', 'is_active']
