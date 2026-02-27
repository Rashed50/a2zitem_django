import uuid, json, random, datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

##? Utils Import
from core.utils.generator import generate_unique_slug, generate_unique_code

##? Models Import
User = get_user_model() 
from core.models.time_stamped import TimestampedModel


class Color(TimestampedModel):
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name=_("Color Name"))
    
    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")
        ordering = ['name']
        
    def __str__(self):
        return self.name