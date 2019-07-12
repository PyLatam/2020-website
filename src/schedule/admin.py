from django.contrib import admin

from .models import Event, Speaker, Talk, TimeSlot


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_filter = ['room', 'language']
    list_display = ['speaker', 'title', 'room', 'language']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'start_time', 'end_time', 'duration']
