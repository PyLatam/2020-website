from django.contrib import admin

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

    def has_account(self, obj):
        if obj.account_id:
            return True
        return Account.objects.filter(user__email=obj.email).exists()

    def has_registration(self, obj):
        lookup = (
            ConferenceRegistration
            .objects
            .filter(account__user__email=obj.email)
        )
        return lookup.exists()


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_filter = ['room', 'language']
    list_display = ['speaker', 'title', 'room', 'language', 'time_slot']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'start_time', 'end_time', 'duration']
