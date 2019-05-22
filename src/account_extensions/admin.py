from django.contrib import admin

from account.admin import AccountAdmin as BaseAccountAdmin
from account.models import Account


class AccountAdmin(BaseAccountAdmin):
    list_display = ['username', 'user_email', 'user_date_joined']
    ordering = ('-user__date_joined',)

    def username(self, obj):
        return obj.user.username

    def user_email(self, obj):
        return obj.user.email

    def user_date_joined(self, obj):
        return obj.user.date_joined


admin.site.unregister(Account)
admin.site.register(Account, AccountAdmin)
