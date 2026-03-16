from django.contrib import admin

##? Models Import
from apps.sales.models.sale import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone', 'address')

