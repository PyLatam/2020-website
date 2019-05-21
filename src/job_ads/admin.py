from django.contrib import admin

from .models import JobAd


@admin.register(JobAd)
class JobAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'is_active']
