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

class Sale(TimestampedModel2):
    invoice_no = models.CharField(max_length=50, unique=True, verbose_name=_("Invoice Number"))
    customer   = models.ForeignKey(
        User,
        on_delete    = models.SET_NULL,
        null         = True,
        blank        = True,
        related_name = "sales",
        verbose_name = _("Customer")
    )

    sale_date  = models.DateTimeField(default=timezone.now, verbose_name=_("Order Date"))
    notes      = models.TextField(blank=True, null=True, verbose_name=_("Notes"))

    grand_total = models.DecimalField(
        max_digits     = 14,
        decimal_places = 2,
        default        = 0.00,
        editable       = False,
        verbose_name   = _("Grand Total")
    )

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")
        ordering = ["-sale_date"]

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = generate_unique_code(
                model_class = Sale,
                prefix      = "INV",
                field_name  = "invoice_no",
                padding     = 10
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_no

    def update_grand_total(self):
        self.grand_total = sum(
            item.subtotal for item in self.items.all()
        )
        self.save(update_fields=["grand_total"])