from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Religion(models.Model):
    name = models.CharField(
        verbose_name =_("Religion Name"),
        max_length   = 50,
        unique       = True
    )
    slug = models.SlugField(
        verbose_name = _("Slug"),
        unique       = True,
        blank        = True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ReligionDenomination(models.Model):
    religion = models.ForeignKey(
        Religion,
        related_name = 'denominations',
        on_delete    = models.CASCADE,
        verbose_name = _("Religion")
    )
    slug = models.SlugField(blank=True, verbose_name=_("Slug"))
    name = models.CharField(max_length=50, verbose_name=_("Denomination Name"))

    class Meta:
        unique_together = ('religion', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.religion.name})"
