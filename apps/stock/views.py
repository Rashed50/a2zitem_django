from django.shortcuts import render

# Create your views here.
from django.db import transaction
from apps.stock.models import StockMovement


# @transaction.atomic
# def process_purchase(purchase):

#     total = 0

#     for item in purchase.items.all():
#         variant = item.variant

#         # Increase stock
#         variant.quantity += item.quantity
#         variant.save()

#         # Create stock log
#         StockMovement.objects.create(
#             variant=variant,
#             movement_type=StockMovement.STOCK_IN,
#             quantity=item.quantity,
#             reference=purchase.invoice_no
#         )

#         total += item.subtotal

#     purchase.total_amount = total
#     purchase.save()