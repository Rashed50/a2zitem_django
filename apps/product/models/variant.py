import uuid, json, random, datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

##? Utils Import
from core.utils.generator import generate_unique_slug, generate_unique_code

##? Models Import
User = get_user_model() 
from core.models.time_stamped import TimestampedModel, TimestampedModel2
from apps.product.models.product import Product
from apps.product.models.category import Category
from apps.product.models.brand import Brand
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.color import Color
from apps.product.models.size import Size


class ProductVariant(TimestampedModel2):
    product = models.ForeignKey(
        Product,
        on_delete    = models.CASCADE,
        related_name = "variants"
    )

    sku = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=_("Stock Keeping Unit (SKU)"))
    
    stock     = models.PositiveIntegerField(default=0, verbose_name=_("Stock Quantity"))
    min_stock = models.PositiveIntegerField(default=0, verbose_name=_("Minimum Stock"))

    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Color"))
    size  = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Size"))
    unit  = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Unit"))
    
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Purchase Price"))
    selling_price  = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Selling Price"))

    is_default = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name        = _("Product Variant")
        verbose_name_plural = _("Product Variants")
        ordering            = ['-created_at', '-updated_at']

        ##* This will ensure that the same Color + Size of the same Product cannot be inserted twice.
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'],
                name='unique_variant_per_product'
            )
        ]

    def __str__(self):
        return f"{self.product.title} - {self.sku}"
    
    def clean(self):
        ##* Price validation
        if self.selling_price < self.purchase_price:
            raise ValidationError("Selling price cannot be less than purchase price.")

        ##* Default variant validation
        if self.is_default:
            qs = ProductVariant.objects.filter(product=self.product, is_default=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Only one default variant allowed per product")
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_low_stock(self):
        return self.stock <= self.min_stock