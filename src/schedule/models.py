from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import get_language
from django.urls import reverse

from filer.fields.image import FilerImageField

from account.models import Account


AUDIENCE_CHOICES = (
    ('all', 'All'),
    ('beginners', 'Beginner'),
    ('medium', 'Intermediate'),
)


ROOM_CHOICES = (
    # Talk rooms
    ('room_en', 'Concha Nacar 1'),
    ('room_es', 'Concha Nacar 2'),
    # Lunch & breakfast rooms
    ('lunch', 'El Palmar & Villa Linda'),
    ('breakfast', 'El Palmar & Villa Linda'),
)


class TimeSlot(models.Model):
    start = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text='In minutes')

    class Meta:
        ordering = ('start',)

    def __str__(self):
        return f'{self.start_date.day}: {self.start_time} - {self.end_time}'

    @cached_property
    def start_date(self):
        return timezone.localtime(self.start).date()

    @cached_property
    def start_time(self):
        return timezone.localtime(self.start).time()

    @cached_property
    def end_time(self):
        start = timezone.localtime(self.start)
        return (start + timedelta(minutes=self.duration)).time()

    def get_entries(self):
        if self.events.exists():
            # TODO: Optimize
            return self.events.all()
        return self.talks.order_by('language')


class Event(models.Model):
    title_es = models.CharField(max_length=250)
    title_en = models.CharField(max_length=250)
    room = models.CharField(
        max_length=30,
        choices=ROOM_CHOICES,
        blank=True,
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.PROTECT,
        related_name='events',
    )

    class Meta:
        ordering = ('room',)

    def __str__(self):
        return self.title

    @property
    def title(self):
        language = get_language()
        return getattr(self, 'title_{}'.format(language))


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
    is_keynote = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('talk_view', args=[self.slug])


class Speaker(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    bio_es = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)
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

    @property
    def bio(self):
        language = get_language()
        return getattr(self, 'bio_{}'.format(language))
