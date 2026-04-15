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
from apps.product.models.brand import Brand
from apps.product.models.category import Category
from apps.product.models.product import ProductImage
from apps.product.models.product import Product
from apps.product.models.variant import ProductVariant
from apps.product.models.color import Color


##TODO:- Serializers Initialization
class MiniCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ["id", "name"]
                  
class MiniBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Brand
        fields = ['id', 'name']
    
class MiniColorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Color
        fields = ['id', 'name']
        
                              
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductImage
        fields = [
            'id',
            'image',
        ]
        
        
class ProductVariantSerializer(serializers.ModelSerializer):
    id    = serializers.IntegerField(required=False)
    color = MiniColorSerializer(read_only=True)
    # size  = MiniSizeSerializer(read_only=True)
    # unit  = MiniUnitOfMeasureSerializer(read_only=True)
    
    class Meta:
        model  = ProductVariant
        fields = [
            'id', 'sku', 'stock', 'min_stock','color',
            'purchase_price', 'selling_price','is_default',
        ]

class ProductListSerializer(serializers.ModelSerializer):
    category   = MiniCategorySerializer(read_only=True)
    brand      = MiniBrandSerializer(read_only=True)
    images     = ProductImageSerializer(many=True, read_only=True)

    variants = ProductVariantSerializer(many=True, required=False)
    
    class Meta:
        model  = Product
        fields = [
            'id', 'slug', 'code',
            'name',
            'title',
            'category',
            'brand', 
            'is_featured', 
            'is_active', 
            
            'description',
            'images',
            'variants',
        ]





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

class ProductDetailsSerializer(serializers.ModelSerializer):
    category   = MiniCategorySerializer(read_only=True)
    brand      = MiniBrandSerializer(read_only=True)
    images     = ProductImageSerializer(many=True, read_only=True)
    
    variants = ProductVariantSerializer(many=True, required=False)
    related_products = serializers.SerializerMethodField()
    
    class Meta:
        model  = Product
        fields = [
            'id', 'slug', 'code',
            'name',
            'title',
            'category', 'category_id',
            'brand', 'brand_id',
            'is_featured', 
            'is_active', 
            
            'description',
            'images',
            'variants',
            'related_products',
        ]
    
    def get_related_products(self, obj):
        products = Product.objects.filter(
            category=obj.category, is_deleted=False
        ).exclude(id=obj.id)[:2]

        return ProductMiniSerializer(products, many=True).data
    
    
    
    
    
    
    
    
    