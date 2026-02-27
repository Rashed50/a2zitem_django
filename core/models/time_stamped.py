from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

class TimestampedModel(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Time"))
    created_by  = models.ForeignKey(
            settings.AUTH_USER_MODEL,       ##? Lazy reference to User Model
            on_delete    = models.SET_NULL, 
            null         = True, 
            blank        = True, 
            related_name = '%(class)s_created_by',
            verbose_name = _("Created Person")
        )
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated Time"), null=True, blank=True)
    updated_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,       ##? Lazy reference to User Model
            on_delete    = models.SET_NULL, 
            null         = True, 
            blank        = True, 
            related_name = '%(class)s_updated_by',
            verbose_name = _("Last Updated Person")
        )
    
    is_active   = models.BooleanField(default=True, verbose_name=_("Active"))
    is_deleted  = models.BooleanField(default=False, verbose_name=_("Deleted"))

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']



class TimestampedModel2(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Time"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated Time"), null=True, blank=True)
    is_active  = models.BooleanField(default=True, verbose_name=_("Active"))
    
    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

