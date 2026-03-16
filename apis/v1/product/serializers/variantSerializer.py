from rest_framework import serializers 
from django.conf import settings 

from django.db import transaction 
from django.db.models import Q, F, Count, Value, Prefetch 
from django.contrib.auth import get_user_model 
from django.utils.timezone import localtime 

##? Utils Importn 
from apis.utils.field_error_messages import get_field_error_messages 
from apis.utils.apiResponse import * 

##? Models Importn
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.product import Product
from apps.product.models.variant import ProductVariant

##? Serializers Import
from apis.v1.attributes.serializers.brandSerializer import MiniBrandSerializer
from apis.v1.attributes.serializers.categorySerializer import MiniCategorySerializer
from apis.v1.attributes.serializers.colorSerializer import MiniColorSerializer
from apis.v1.attributes.serializers.sizeSerializer import MiniSizeSerializer
from apis.v1.attributes.serializers.unitSerializer import MiniUnitOfMeasureSerializer
# from apis.v1.product.serializers.productSerializer import ProductMiniSerializer

class ProductVariantSerializer(serializers.ModelSerializer):
    id    = serializers.IntegerField(required=False)
    color = MiniColorSerializer(read_only=True)
    size  = MiniSizeSerializer(read_only=True)
    unit  = MiniUnitOfMeasureSerializer(read_only=True)
    
    color_id = serializers.PrimaryKeyRelatedField(
        queryset   = Color.objects.all(),
        source     = 'color',
        write_only = True,
        required   = True,
        allow_null = False,
        error_messages = get_field_error_messages('Color', 'PrimaryKeyRelated'),
    )
    size_id = serializers.PrimaryKeyRelatedField(
        queryset   = Size.objects.all(),
        source     = 'size',
        write_only = True,
        required   = True,
        allow_null = False,
        error_messages=get_field_error_messages('Size', 'PrimaryKeyRelated'),
    )
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset   = UnitOfMeasure.objects.all(),
        source     = 'unit',
        write_only = True,
        required   = True,
        allow_null = False,
        error_messages=get_field_error_messages('Unit', 'PrimaryKeyRelated'),
    )
    
    class Meta:
        model  = ProductVariant
        fields = [
            'id', 'sku', 'stock', 'min_stock',
            'color', 'color_id',
            'size', 'size_id',
            'unit', 'unit_id',
            'purchase_price', 'selling_price',
            'is_default',
        ]
        read_only_fields = ['sku']
        extra_kwargs = {
            'stock': {
                'required': True,
                'error_messages': get_field_error_messages('Stock', 'IntegerField')
            },
            'selling_price': {
                'required': True,
                'error_messages': get_field_error_messages('Selling price', 'DecimalField')
            },
            'purchase_price': {
                'required': False,
                'allow_null': True,
                'default': 0,
            },
        }
    
    def validate(self, data):
        """
        Validate variant data
        """
        # Set default values if not provided
        if 'purchase_price' not in data or data['purchase_price'] is None:
            data['purchase_price'] = 0
            
        if 'min_stock' not in data or data['min_stock'] is None:
            data['min_stock'] = 0
            
        if 'stock' not in data or data['stock'] is None:
            data['stock'] = 0
            
        return data
    
   
   
class ProductMiniSerializer(serializers.ModelSerializer):
    category = MiniCategorySerializer(read_only=True)
    brand    = MiniBrandSerializer(read_only=True)
    class Meta:
        model  = Product
        fields = [
            'id', 
            'slug', 
            'code',
            'name',
            'title',
            'category',
            'brand', 
        ]
    
class VariantMiniListSerializer(serializers.ModelSerializer):
    color   = MiniColorSerializer()
    size    = MiniSizeSerializer()
    unit    = MiniUnitOfMeasureSerializer()
    product = ProductMiniSerializer()
    class Meta:
        model  = ProductVariant
        fields = [
            'id', 
            'sku', 
            'color', 
            'size', 
            'unit', 
            'stock', 
            'min_stock', 
            'selling_price', 
            'product',
        ]
        
    