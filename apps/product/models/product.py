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
from apps.product.models.catagory import Catagory
from apps.product.models.brand import Brand


class ProductName(TimestampedModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Item Name"))
    logo = models.ImageField(upload_to='products/logos/', null=True, blank=True, verbose_name=_("Item Logo"))
    
    class Meta:
        verbose_name = _("Product Name")
        verbose_name_plural = _("Product Names")
        
    def __str__(self):
        return self.name
    

class Product(TimestampedModel):
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name=_("Slug"))
    code = models.CharField(max_length=20, unique=True, blank=True, verbose_name=_("Product Code"))
    
    name = models.ForeignKey(
            ProductName, 
            on_delete    = models.CASCADE, 
            related_name = 'products', 
            verbose_name = _("Product Name")
        )
    
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
    
    title       = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    pur_price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Purchase Price"))
    sell_price      = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Selling Price"))
    quantity        = models.PositiveIntegerField(default=0, verbose_name=_("Quantity"))
    

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name)
        if not self.code:
            self.code = generate_unique_code(Product, length=8)
        super().save(*args, **kwargs)
    