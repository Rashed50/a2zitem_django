import uuid, json, random, datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

##? Utils Import
from core.utils.generator import generate_unique_slug, generate_unique_code

##? Models Import
User = get_user_model() 
from core.models.time_stamped import TimestampedModel, TimestampedModel2
from apps.sales.models.sale import Sale
from apps.product.models.variant import ProductVariant

class SaleItem(TimestampedModel2):
    sale = models.ForeignKey(
        Sale,
        on_delete    = models.CASCADE,
        related_name = "items",
        verbose_name = _("Sale")
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete    = models.PROTECT,
        related_name = "sale_items",
        verbose_name = _("Product Variant")
    )

    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        verbose_name = _("Sale Item")
        verbose_name_plural = _("Sale Items")
        unique_together = ['sale', 'variant']
        
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
        
        # reduce stock
        self.variant.stock -= self.quantity
        self.variant.save(update_fields=["stock"])

        self.sale.update_grand_total()


        