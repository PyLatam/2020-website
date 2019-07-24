from django.conf import settings
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _

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


class Tier(models.Model):
    name_es = models.CharField(max_length=120)
    name_en = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    @property
    def name(self):
        language = get_language()
        return getattr(self, 'name_{}'.format(language))


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
    tiers = models.ManyToManyField(Tier)

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name


class SponsorsListPlugin(CMSPlugin):
    level = models.CharField(max_length=12, choices=SPONSORSHIP_LEVELS)
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.tier.name
