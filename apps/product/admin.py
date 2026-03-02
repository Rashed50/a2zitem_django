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
    list_display = ['id', 'slug', 'name']
    search_fields = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}
   
@admin.register(Color) 
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']

@admin.register(Size) 
class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    
@admin.register(UnitOfMeasure)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'full_name']
    search_fields = ['id', 'name', 'full_name']

# @admin.register(Category) 
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'parent__name']
#     search_fields = ['id', 'name', 'parent__name']


@admin.register(Category)
class CatagoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)