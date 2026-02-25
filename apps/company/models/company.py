import uuid, json, random, datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

##? Import Users
User = get_user_model() 

##? Import TimestampedModel 
from core.models.time_stamped import TimestampedModel

##? Import Utils
from core.utils.generator import generate_unique_slug, generate_unique_code


class Company(TimestampedModel):
    """Main Company for Multi-Vendor POS"""
    class CompanyType(models.TextChoices):
        PRIVATE     = "private",    _("Private")
        PUBLIC      = "public",     _("Public")
        GOVERNMENT  = "government", _("Government")
        
    slug       = models.SlugField(unique=True, blank=True, verbose_name=_("Slug"))
    name       = models.CharField(max_length=255, unique=True, verbose_name=_("Company Name"))
    short_name = models.CharField(max_length=255, unique=True, null=True, verbose_name=_("Company Short Name"))
    code       = models.CharField(max_length=20, unique=True, db_index=True, verbose_name=_("Company Code Number"),
                        help_text=_("Short unique company identifier (e.g. ABCD, AB001)")
                    )

    company_type = models.CharField(max_length=20, choices=CompanyType.choices, default=CompanyType.PRIVATE, verbose_name=_("Company Type"))
        
    email   = models.EmailField(null=True, blank=True, verbose_name=_("Company Email"))
    phone   = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Company Phone"))
    website = models.URLField(null=True, blank=True, verbose_name=_("Company Website"))
    logo    = models.ImageField(upload_to="company/logo/", null=True, blank=True, verbose_name=_("Company Logo"))
    gov_license = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Government License Number"))
    address = models.TextField(null=True, blank=True, verbose_name=_("Company Address"))
    
    established_at = models.DateField(blank=True, null=True, verbose_name=_("Established At"))

    metadata = models.JSONField(
            default = dict,
            blank   = True,
            verbose_name = _("Company Metadata"),
            help_text    = _("Flexible field for company-specific settings.")
        )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate unique slug and code_no"""
        ##? Slut Auto Generate
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
            
        ##? Code Auto Generate
        if not self.code:
            prefix = (self.short_name.upper()if self.short_name else self.name[:2].upper())
            prefix = prefix.replace(" ", "").replace("-", "") ## Clean prefix (safe)
            self.code = generate_unique_code(Company, prefix=prefix, field_name="code", padding=6)
        super().save(*args, **kwargs)