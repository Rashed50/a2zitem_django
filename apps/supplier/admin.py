from django.contrib import admin

##? Models Import
from apps.supplier.models import Supplier



##TODO- Register Models

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'contact', 'email', 'phone', 'is_active']
    search_fields = ['name', 'contact', 'email', 'phone', 'address']
    ordering      = ['-created_at',]
