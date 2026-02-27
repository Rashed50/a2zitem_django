from django.db import models
from django.utils.translation import gettext_lazy as _

##? Import Utils
from core.utils.generator import generate_unique_slug, generate_unique_code

##? Models Import
from core.models.time_stamped import TimestampedModel2


class Country(TimestampedModel2):
    slug       = models.SlugField(
        max_length   = 255,
        unique       = True,
        db_index     = True,
        blank        = True, 
        verbose_name = _("Slug")
    )
    
    name       = models.CharField(
        max_length   = 100,  
        unique       = True,
        db_index     = True,
        verbose_name = _("Country Name")
    )
    
    code = models.CharField(
        max_length   = 10, 
        unique       = True, 
        verbose_name = _("Country Code")
    )

    capital    = models.CharField(max_length=100, blank=True, null=True, verbose_name = _("Capital"))
    region     = models.CharField(max_length=5, blank=True, null=True, verbose_name = _("Region"))

    cur_code   = models.CharField(max_length=10, blank=True, null=True, verbose_name = _("Currency Code"))
    cur_name   = models.CharField(max_length=50, blank=True, null=True, verbose_name = _("Currency Name"))
    cur_symbol = models.CharField(max_length=10, blank=True, null=True, verbose_name = _("Currency Symbol"))

    lan_code   = models.CharField(max_length=10, blank=True, null=True, verbose_name = _("Language Code"))
    lan_name   = models.CharField(max_length=50, blank=True, null=True, verbose_name = _("Language Name"))

    dia_code   = models.CharField(max_length=10, blank=True, null=True, verbose_name = _("Dialling Code"))
    iso_code   = models.CharField(max_length=10, blank=True, null=True, verbose_name = _("ISO Code"))
    flag       = models.ImageField(upload_to='flags/', blank=True, null=True, verbose_name = _("Flag"))

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

class State(TimestampedModel2):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class City(TimestampedModel2):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name  = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
