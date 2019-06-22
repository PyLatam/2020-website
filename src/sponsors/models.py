from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from cms.models import CMSPlugin

from model_utils import Choices


SPONSORSHIP_LEVELS = Choices(
    ('basic', _('Basic')),
    ('bronze', _('Bronze')),
    ('silver', _('Silver')),
    ('gold', _('Gold')),
    ('diamond', _('Diamond')),
    ('tshirt', _('T-Shirt')),
)


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
    level = models.CharField(
        max_length=12,
        choices=SPONSORSHIP_LEVELS,
        default=SPONSORSHIP_LEVELS.basic,
    )

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name


class SponsorsListPlugin(CMSPlugin):
    level = models.CharField(max_length=12, choices=SPONSORSHIP_LEVELS)

    def __str__(self):
        return self.level
