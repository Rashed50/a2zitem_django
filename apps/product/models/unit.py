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


class UnitOfMeasure(TimestampedModel): 
    name      = models.CharField(max_length=100, unique=True, db_index=True, verbose_name=_("Unit Name"))
    full_name = models.CharField(max_length=10, unique=True, verbose_name=_("Unit Full Name"))
    
    class Meta:
        verbose_name = _("Unit of Measure")
        verbose_name_plural = _("Units of Measure")
        unique_together = ['name', 'full_name']
    
    def __str__(self):
        return f"{self.name} ({self.full_name})"