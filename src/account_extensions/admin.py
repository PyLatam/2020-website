from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from account.admin import AccountAdmin as BaseAccountAdmin
from account.models import Account

from core.models import ConferenceRegistration


class AccountAdmin(BaseAccountAdmin):
    list_display = ['username', 'user_email', 'user_date_joined']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering = ('-user__date_joined',)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj=obj))

        if obj:
            fields.append('conference_registration')
        return fields

    def username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def user_date_joined(self, obj):
        return obj.user.date_joined

    def conference_registration(self, obj):
        registration = ConferenceRegistration.get_for_user(obj.user)

        if not registration:
            return ''
        admin_link = reverse('admin:core_conferenceregistration_change', args=(registration.pk,))
        return format_html('<br /><a href="{}" target="_target">{}</a>', admin_link, 'View')


admin.site.unregister(Account)
admin.site.register(Account, AccountAdmin)
