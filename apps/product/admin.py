from django.contrib import admin
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html

from mptt.admin import DraggableMPTTAdmin

##? Models Import
from apps.product.models.product import Product
from apps.product.models.variant import ProductVariant
from apps.product.models.brand import Brand
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.category import Category

class ProductVariantInline(admin.TabularInline):
    model   = ProductVariant
    extra   = 1 
    min_num = 1  
    max_num = 10  
    
    fields = [
        'sku', 
        'color', 
        'size', 
        'unit', 
        'stock', 
        'min_stock', 
        'purchase_price', 
        'selling_price', 
        'is_default'
    ]
    
    readonly_fields     = ['sku']  
    autocomplete_fields = ['color', 'size', 'unit']  

    # classes = ['collapse']  
    
    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return self.readonly_fields + ['sku']
        return self.readonly_fields
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "color":
            kwargs["queryset"] = Color.objects.filter(is_active=True)
        elif db_field.name == "size":
            kwargs["queryset"] = Size.objects.filter(is_active=True)
        elif db_field.name == "unit":
            kwargs["queryset"] = UnitOfMeasure.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines       = [ProductVariantInline]
    list_display  = ['id', 'slug', 'name', 'title', 'category__name', 'brand__name', 'is_active', 'is_deleted', 'formatted_created_at']
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['created_by', 'updated_by', 'brand', 'category']
    
    # Create At (DD-MM-YYYY)
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d-%b-%Y')
    formatted_created_at.short_description = 'Created At'
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'product__name', 'color__name', 'size__name', 'selling_price', 'stock', 'is_active', 'created_at']
    search_fields = ['id', 'product__name', 'color__name', 'size__name']
    autocomplete_fields = ['product', 'color', 'size', 'unit',]
    

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'name', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['created_by', 'updated_by']
   
@admin.register(Color) 
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['id', 'name']
    autocomplete_fields = ['created_by', 'updated_by']

@admin.register(Size) 
class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['id', 'name']
    autocomplete_fields = ['created_by', 'updated_by']
    
@admin.register(UnitOfMeasure)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['id', 'name', 'symbol']
    autocomplete_fields = ['created_by', 'updated_by']

# @admin.register(Category) 
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'parent__name']
#     search_fields = ['id', 'name', 'parent__name']


@admin.register(Category)
class CatagoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'id',
        'tree_actions',
        'indented_title',
        'slug',
        'is_active',
        'is_deleted',
        'created_at'
    )

    list_display_links  = ('indented_title',)
    search_fields       = ['name', 'slug',]
    autocomplete_fields = ['created_by', 'updated_by', 'parent']
    # autocomplete_fields = ['created_by', 'updated_by',] 
    mptt_level_indent   = 20