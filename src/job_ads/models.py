from django.db import models

from filer.fields.image import FilerImageField


class JobAd(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)
    company_logo = FilerImageField(on_delete=models.PROTECT)
    url = models.URLField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
