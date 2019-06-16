from django.conf import settings
from django.db import models

from filer.fields.image import FilerImageField


class Sponsor(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(blank=False)
    logo = FilerImageField(on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'is_staff': True},
    )
    position = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name
