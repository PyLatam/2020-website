from django.contrib import admin

from .models import Event, Speaker, Talk, TimeSlot


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'room', 'time_slot']


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'account']
    raw_id_fields = ['account']


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_filter = ['room', 'language']
    list_display = ['speaker', 'title', 'room', 'language', 'time_slot']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'start_time', 'end_time', 'duration']
