from django.contrib import admin

##? Models Import
from apps.product.models.brand import Brand
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.category import Catagory

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

@admin.register(Catagory) 
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent__name']
    search_fields = ['id', 'name', 'parent__name']

