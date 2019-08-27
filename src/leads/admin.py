from django.contrib import admin
from django.utils.html import format_html

from .models import Lead, LeadCode, LeadGroup


class LeadInline(admin.TabularInline):
    model = Lead
    fields = ['account_name', 'created_on']
    readonly_fields = fields

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def account_name(self, obj):
        return obj.account.user.get_full_name()


@admin.register(LeadCode)
class LeadCodeAdmin(admin.ModelAdmin):
    fields = ['account', 'account_name', 'account_email', 'code_image_display']
    readonly_fields = fields
    list_display = ['account', 'account_name', 'account_email']
    search_fields = [
        'account__user__first_name',
        'account__user__last_name',
        'account__user__email',
    ]

    def has_add_permission(self, request):
        return False

    def account_name(self, obj):
        return obj.account.user.get_full_name()

    def account_email(self, obj):
        return obj.account.user.email

    def code_image_display(self, obj):
        if not obj.code_image:
            return ''
        return format_html('<img src="{url}" />', url=obj.code_image.url)


@admin.register(LeadGroup)
class LeadGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['admins']
    inlines = [LeadInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        formfield = super().formfield_for_manytomany(db_field, request, **kwargs)

        if db_field.name == 'admins':
            formfield.label_from_instance = lambda account: account.user.email
        return formfield
