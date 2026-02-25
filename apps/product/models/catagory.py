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



class Catagory(TimestampedModel):
    slug   = models.SlugField(max_length=255, unique=True, verbose_name=_("Slug"))
    name   = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    logo   = models.ImageField(upload_to='catagories/logos/', null=True, blank=True, verbose_name=_("Logo"))
    parent = models.ForeignKey(
            'self', 
            on_delete    = models.SET_NULL, 
            null         = True, 
            blank        = True, 
            related_name = 'children', 
            verbose_name = _("Parent Catagory")
        )

    class Meta:
        verbose_name = _("Catagory")
        verbose_name_plural = _("Catagories")
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Catagory, self.name)
        super().save(*args, **kwargs)