import uuid, json, random, datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

##? Import Utils
from core.utils.generator import generate_unique_slug, generate_unique_code

##? Import Users
User = get_user_model() 
from core.models.time_stamped import TimestampedModel
from apps.product.models.variant import ProductVariant


class StockMovement(TimestampedModel):
    class MovementType(models.TextChoices):
        IN  = "in", _("Stock In")
        OUT = "out", _("Stock Out")
    
    movement_type = models.CharField(
            max_length   = 10, 
            choices      = MovementType.choices, 
            default      = MovementType.IN, 
            verbose_name = _("Movement Type")
        )
    
    variant = models.ForeignKey(
            ProductVariant,
            on_delete    = models.CASCADE,
            related_name = "stock_movements",
            verbose_name = _("Product Variant")
        )

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    note     = models.TextField(blank=True, null=True, verbose_name=_("Note"))
    
    class Meta:
        verbose_name = _("Stock Movement")
        verbose_name_plural = _("Stock Movements")
        ordering = ["-created_at"]
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.movement_type == self.MovementType.IN:
            self.variant.stock += self.quantity
        else:
            self.variant.stock -= self.quantity

        self.variant.save(update_fields=["stock"])
    
    def __str__(self):
        return f"{self.variant} {self.movement_type} {self.quantity}"