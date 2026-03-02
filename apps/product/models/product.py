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
from core.models.time_stamped import TimestampedModel, TimestampedModel2
from apps.product.models.category import Catagory
from apps.product.models.brand import Brand 

class Product(TimestampedModel):
    slug  = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, verbose_name=_("Slug"))
    code  = models.CharField(max_length=20, unique=True, db_index=True, blank=True, verbose_name=_("Product Code"))
    name  = models.CharField(max_length=255, unique=True, db_index=True, verbose_name=_("Item Name"))
    title = models.CharField(max_length=255, db_index=True, verbose_name=_("Title"))
    
    catagory = models.ForeignKey(
            Catagory, 
            on_delete = models.SET_NULL, 
            null      = True, 
            blank     = True, 
            related_name = 'products', 
            verbose_name = _("Catagory")
        )
    
    brand = models.ForeignKey(
            Brand, 
            on_delete = models.SET_NULL, 
            null      = True, 
            blank     = True, 
            related_name = 'products', 
            verbose_name = _("Brand")
        )
    
    description    = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    is_featured    = models.BooleanField(default=False)
    
    metadata = models.JSONField(
            default = dict,
            blank   = True,
            verbose_name = _("Company Metadata"),
            help_text    = _("Flexible field for company-specific settings.")
        )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.title)
        if not self.code:
            self.code = generate_unique_code(Product, length=8)
        super().save(*args, **kwargs)
    
    
    
    
class ProductImage(TimestampedModel2):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("Product"))
    image      = models.ImageField(upload_to='products/images/', verbose_name=_("Image"))
    alt_text   = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Alt Text"))
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"Image for {self.product.title}"
    
    
    
    
    