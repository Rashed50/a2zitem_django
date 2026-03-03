from django.contrib import admin

##? Models Import
from apps.supplier.models import Supplier



##TODO- Register Models

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'contact', 'email', 'phone', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['name', 'contact', 'email', 'phone', 'address']
    ordering      = ['-created_at',]
    autocomplete_fields = ['created_by', 'updated_by']
