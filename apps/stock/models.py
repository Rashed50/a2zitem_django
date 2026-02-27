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


class StockLog(TimestampedModel):
    PRODUCT_IN  = "IN"
    PRODUCT_OUT = "OUT"

    MOVEMENT_TYPE = (
        (PRODUCT_IN, "Stock In"),
        (PRODUCT_OUT, "Stock Out"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_logs"
    )

    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE)
    quantity      = models.PositiveIntegerField()
    note          = models.TextField(blank=True, null=True)