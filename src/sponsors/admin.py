from django.contrib import admin

from .models import Sponsor, Tier


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    fields = ['name', 'tiers', 'position', 'website', 'contact', 'logo', 'is_active']


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    fields = ['name_es', 'name_en']
    list_display = ['name']
