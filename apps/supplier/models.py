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


class Supplier(TimestampedModel):
    slug    = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, verbose_name=_("Slug"))
    name    = models.CharField(max_length=255, unique=True, db_index=True, verbose_name=_("Supplier Company Name"))
    contact = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Contact Person"))
    email   = models.EmailField(max_length=255, blank=True, null=True, verbose_name=_("Supplier Email"))
    phone   = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Supplier Phone"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Supplier Address"))
    
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)