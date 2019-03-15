from django.db import models
from django.utils.functional import cached_property

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
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='registration',
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.PROTECT,
        related_name='registrations',
    )
    created = models.DateTimeField(
        verbose_name='creation date',
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.reservation.email

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
