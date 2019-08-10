from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from account.models import Account

from . import constants


class Reservation(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    number = models.IntegerField(unique=True)
    active = models.BooleanField(default=True)
    checkin = models.DateField()
    checkout = models.DateField()
    occupancy = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.email

    def has_vacancies(self):
        return self.occupancy > self.registrations.count()


class ConferenceRegistration(models.Model):
    SHIRT_SIZES = (
        ("Men-S", _("Men's S")),
        ("Men-M", _("Men's M")),
        ("Men-L", _("Men's L")),
        ("Men-XL", _("Men's XL")),
        ("Men-2XL", _("Men's 2XL")),
        ("Men-3XL", _("Men's 3XL")),
        ("Men-4XL", _("Men's 4XL")),
        ("Women-S", _("Women's S")),
        ("Women-M", _("Women's M")),
        ("Women-L", _("Women's L")),
        ("Women-XL", _("Women's XL")),
        ("Women-2XL", _("Women's 2XL")),
        ("Women-3XL", _("Women's 3XL")),
        ("Women-4XL", _("Women's 4XL")),
    )

    RESERVATION_TYPES = (
        ('default', 'Default'),
        ('sponsor', 'Sponsor'),
        ('grant-recipient', 'Grant Recipient'),
        ('internal', 'Internal'),
    )

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='registration',
    )
    reservation = models.ForeignKey(
        Reservation,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='registrations',
    )
    created = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True,
        editable=False,
    )
    shirt_size = models.CharField(
        max_length=30,
        choices=SHIRT_SIZES,
        blank=True,
        default='',
    )
    reservation_type = models.CharField(
        max_length=30,
        choices=RESERVATION_TYPES,
        default='default',
    )
    needs_translation_device = models.NullBooleanField(default=None)
    joining_sponsor_presentation = models.NullBooleanField(default=None)

    class Meta:
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return str(self.pk)

    @classmethod
    def get_for_user(cls, user):
        return cls.objects.filter(account__user=user).last()

    @classmethod
    def exists_for_user(cls, user):
        return cls.objects.filter(account__user=user).exists()

    @property
    def ready(self):
        return not bool(self.missing)

    @cached_property
    def missing(self):
        return self.get_missing_info()

    def get_missing_info(self):
        missing = []

        if not self.account.user.get_full_name():
            missing.append(constants.FULL_NAME_REQUIRED)
        return missing
