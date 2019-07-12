from django.contrib import admin
from django.db.models import Count

from .models import ConferenceRegistration, Reservation


@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['account_name', 'account_email']
    list_filter = ['is_sponsor', 'is_grant_recipient']
    search_fields = [
        'account__user__first_name',
        'account__user__last_name',
        'account__user__email',
    ]
    raw_id_fields = ['account']

    def account_name(self, obj):
        return obj.account.user.get_full_name()

    def account_email(self, obj):
        return obj.account.user.email


class RegistrationInline(admin.StackedInline):
    model = ConferenceRegistration
    fields = ['account_name', 'account_email']
    readonly_fields = fields

    def has_add_permission(self, request, obj):
        return False

    def account_name(self, obj):
        return obj.account.user.get_full_name()

    def account_email(self, obj):
        return obj.account.user.email


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'number',
        'email',
        'checkin',
        'checkout',
        'registration_count',
    ]
    fields = [
        'number',
        'name',
        'email',
        'checkin',
        'checkout',
        'occupancy',
        'created',
    ]
    readonly_fields = fields
    search_fields = ['number', 'email', 'name']
    inlines = [RegistrationInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(registration_count=Count('registrations'))

    def has_add_permission(self, request):
        return False

    def registration_count(self, obj):
        return obj.registration_count
