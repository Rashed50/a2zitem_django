from django.db import models, transaction
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
from apps.product.models.variant import ProductVariant
from apps.sales.models.sale import Sale
from apps.sales.models.item import SaleItem


class Order(TimestampedModel2):

    class Status(models.TextChoices):
        PENDING   = "pending",   _("Pending")
        CONFIRMED = "confirmed", _("Confirmed")
        CANCELLED = "cancelled", _("Cancelled")
        COMPLETED = "completed", _("Completed")

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name=_("Customer"))
    order_no = models.CharField(max_length=50, unique=True, verbose_name=_("Order Number"))
    status   = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Status"))

    grand_total = models.DecimalField(
        max_digits     = 14,
        decimal_places = 2,
        default        = 0,
        editable       = False,
        verbose_name   = _("Grand Total")
    )

    def __str__(self):
        return self.order_no

    def update_grand_total(self):
        self.grand_total = sum(
            item.subtotal for item in self.items.all()
        )
        self.save(update_fields=["grand_total"])
        
    def confirm_order(self):
        if self.status != self.Status.PENDING:
            raise ValidationError("Only pending orders can be confirmed.")

        with transaction.atomic():
            sale = Sale.objects.create(
                customer  = self.customer,
                sale_date = timezone.now()
            )
            for item in self.items.all():
                SaleItem.objects.create(
                    sale     = sale,
                    variant  = item.variant,
                    quantity = item.quantity,
                    price    = item.price
                )
            self.status = self.Status.COMPLETED
            self.save(update_fields=["status"])
        return sale
        
        
        
        
class OrderItem(TimestampedModel2):

    order   = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order"))
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="order_items", verbose_name=_("Product Variant"))

    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        unique_together = ["order", "variant"]

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)
        self.order.update_grand_total()