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
from apps.supplier.models import Supplier
from apps.product.models.variant import ProductVariant
from apps.stock.models import StockMovement


class Purchase(TimestampedModel):
    supplier = models.ForeignKey(
        Supplier,
        on_delete    = models.PROTECT,
        related_name = "purchases",
        verbose_name = _("Supplier")
    )
    
    invoice_no    = models.CharField(max_length=50, unique=True, verbose_name=_("Invoice Number"))
    purchase_date = models.DateField(default=timezone.now, verbose_name=_("Order Date"))
    notes         = models.TextField(blank=True, null=True, verbose_name=_("Notes"))
    
    grand_total   = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, editable=False, verbose_name=_("Grand Total"))

    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")    
        ordering = ['-purchase_date']

    def __str__(self):
        return f"{self.invoice_no}"
    
    def update_grand_total(self):
        self.grand_total = sum(item.subtotal for item in self.items.all() if item.subtotal)
        self.save(update_fields=['grand_total'])
    
    
class PurchaseItem(TimestampedModel2):
    purchase = models.ForeignKey(
        Purchase,
        on_delete    = models.CASCADE,
        related_name = "items",
        verbose_name = _("Purchase Order"),
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete    = models.PROTECT,
        related_name = "purchase_items",
        verbose_name = _("Product Variant"),
    )
    
    expire_date = models.DateField(null=True, blank=True, verbose_name=_("Expire Date"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    price    = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Unit Price"))
    subtotal = models.DecimalField(max_digits=12,decimal_places=2,editable=False, verbose_name=_("Subtotal"))
    
    class Meta:
        verbose_name        = _("Purchase Item")
        verbose_name_plural = _("Purchase Items")
        ordering            = ['-created_at', '-updated_at']
        unique_together     = ['purchase', 'variant']

    def save(self, *args, **kwargs):
        if self.pk:
            old_item = PurchaseItem.objects.get(pk=self.pk)
            diff     = self.quantity - old_item.quantity
        else:
            diff = self.quantity
            
        ##? Step 1: Subtotal Calculation 
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
        
        ##? Step 2: Create Stock Movement (Stock In)
        if diff != 0:
            movement_type = (
                    StockMovement.MovementType.IN
                    if diff > 0
                    else StockMovement.MovementType.OUT
                )
            StockMovement.objects.create(
                variant       = self.variant,
                movement_type = movement_type,
                quantity      = diff,
                note          = f"Purchase {self.purchase.invoice_no}"
            )
        
        ##? Step 3: Update Grand Total
        self.purchase.update_grand_total()
      
    def delete(self, *args, **kwargs):
        StockMovement.objects.create(
            variant       = self.variant,
            movement_type = StockMovement.MovementType.OUT,
            quantity      = self.quantity,
            note          = f"Deleted Purchase {self.purchase.invoice_no}"
        )

        super().delete(*args, **kwargs)
        self.purchase.update_grand_total()
      
    def __str__(self):
        return f"{self.variant} × {self.quantity}"
    

    
    
        