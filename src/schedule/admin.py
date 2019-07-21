from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from account.models import Account
from core.models import ConferenceRegistration

from .models import Event, Speaker, Talk, TimeSlot


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'room', 'time_slot']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'has_account', 'has_registration']
    raw_id_fields = ['account']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate()

    def has_account(self, obj):
        if obj.account_id:
            return True

        if Account.objects.filter(user__email=obj.email).exists():
            return True

        lookup = (
            Account
            .objects
            .annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name'))
            .filter(full_name__iexact=obj.name)
        )
        return lookup.exists()
    has_account.boolean = True

    def has_registration(self, obj):
        if obj.account:
            lookup = ConferenceRegistration.objects.filter(account=obj.account)
            return lookup.exists()
        return False
    has_registration.boolean = True


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_filter = ['room', 'language']
    list_display = ['speaker', 'title', 'room', 'language', 'time_slot']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'start_time', 'end_time', 'duration']
