from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

##? Models Import
from apps.product.models.brand import Brand
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.category import Category

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
    list_display = ['id', 'name', 'full_name', 'is_active', 'is_deleted', 'created_at']
    search_fields = ['id', 'name', 'full_name']
    autocomplete_fields = ['created_by', 'updated_by']

# @admin.register(Category) 
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'parent__name']
#     search_fields = ['id', 'name', 'parent__name']


@admin.register(Category)
class CatagoryAdmin(DraggableMPTTAdmin):
    list_display = ('id', 'tree_actions', 'indented_title', 'slug', 'is_active', 'is_deleted', 'created_at')
    list_display_links = ('indented_title',)
    autocomplete_fields = ['created_by', 'updated_by']