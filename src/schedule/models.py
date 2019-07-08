from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.urls import reverse

from filer.fields.image import FilerImageField

from account.models import Account


AUDIENCE_CHOICES = (
    ('all', 'All'),
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
)


ROOM_CHOICES = (
    # Talk rooms
    ('room_en', 'Nautilus'),
    ('room_es', 'Estrella de mar'),
    # Lunch rooms
    # Breakfast rooms
)


class TimeSlot(models.Model):
    start = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text='In minutes')

    class Meta:
        ordering = ('start',)

    def __str__(self):
        return f'{self.start.day}: {self.start.time()} - {self.end_time}'

    @cached_property
    def start_time(self):
        return self.start.time()

    @cached_property
    def end_time(self):
        return (self.start + timedelta(minutes=self.duration)).time()

    def get_entries(self):
        if self.events.exists():
            # TODO: Optimize
            return self.events.all()
        return self.talks.all()


class Event(models.Model):
    title = models.CharField(max_length=250)
    room = models.CharField(max_length=30, choices=ROOM_CHOICES)
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.PROTECT,
        related_name='events',
    )

    class Meta:
        ordering = ('room',)

    def __str__(self):
        return self.title


class Talk(models.Model):
    title = models.CharField(max_length=250, unique=True)
    room = models.CharField(max_length=30, choices=ROOM_CHOICES)
    slug = models.SlugField()
    abstract = models.TextField()
    description = models.TextField()
    audience_level = models.CharField(max_length=30, choices=AUDIENCE_CHOICES)
    language = models.CharField(
        max_length=15,
        choices=settings.TALK_LANGUAGES,
    )
    speaker = models.ForeignKey(
        'Speaker',
        on_delete=models.PROTECT,
        related_name='proposals',
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='talks',
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('talk_view', args=[self.slug])


class Speaker(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    twitter = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    account = models.ForeignKey(
        Account,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    picture = FilerImageField(
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name
