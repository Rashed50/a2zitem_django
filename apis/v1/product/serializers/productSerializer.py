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

##? Serializers Import
from apis.v1.common.user.serializers import UserMiniListSerializer
from apis.v1.attributes.serializers.brandSerializer import MiniBrandSerializer
from apis.v1.attributes.serializers.categorySerializer import MiniCategorySerializer
from apis.v1.product.serializers.variantSerializer import ProductVariantSerializer


##TODO:- Serializers Initialization
class ProductSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    category   = MiniCategorySerializer(read_only=True)
    brand      = MiniBrandSerializer(read_only=True)
    
    category_hierarchy = serializers.SerializerMethodField(read_only=True)
    category_path      = serializers.SerializerMethodField(read_only=True)
    
    category_id = serializers.PrimaryKeyRelatedField(
            queryset   = Category.objects.all(), 
            source     = "category", 
            write_only = True,
            required   = True,
            allow_null = False,
            error_messages = get_field_error_messages('Category', 'PrimaryKeyRelated'),
        )
    brand_id    = serializers.PrimaryKeyRelatedField(
            queryset   = Brand.objects.all(), 
            source     = "brand", 
            write_only = True,
            required   = True,
            allow_null = False,
            error_messages = get_field_error_messages('Brand', 'PrimaryKeyRelated'),
        )
    
    variants = ProductVariantSerializer(many=True, required=False)
    
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
            
            'created_at', 'updated_at', 'created_by', 'updated_by',
            
            'category_hierarchy', 'category_path',
            
            'description',
            'variants',
        ]
        read_only_fields = [
                'id', 'slug', 'code', 'created_at', 'updated_at', 'created_by', 'updated_by',
            ]
        extra_kwargs = {
            'name' : {
                'required': True, 
                'allow_null': False,
                'allow_blank': False,
                'error_messages': get_field_error_messages('Name', 'CharField')
            },
            'title' : {
                'required': False, 
                'allow_null': True,
                'allow_blank': True,
                'error_messages': get_field_error_messages('Title', 'CharField')
            },
        }
        
    def get_category_hierarchy(self, obj):
        """
        Returns full category hierarchy from root to current category
        Example: [
            {'id': 1, 'name': 'Electronics', 'slug': 'electronics', 'level': 0},
            {'id': 7, 'name': 'Computers', 'slug': 'computers', 'level': 1},
            {'id': 11, 'name': 'Desktops', 'slug': 'desktops', 'level': 2}
        ]
        """
        if not obj.category:
            return []
        
        # Get all ancestors including self
        ancestors = obj.category.get_ancestors(include_self=True)
        
        hierarchy = []
        for ancestor in ancestors:
            hierarchy.append({
                'id': ancestor.id,
                'name': ancestor.name,
                # 'slug': ancestor.slug,
                'level': ancestor.get_level(),
                # 'parent_id': ancestor.parent_id
            })
        
        return hierarchy
    
    def get_category_path(self, obj):
        """
        Returns category path as string
        Example: "Electronics > Computers > Desktops"
        """
        if not obj.category:
            return ""
        
        ancestors = obj.category.get_ancestors(include_self=True)
        return " > ".join([ancestor.name for ancestor in ancestors])


    def validate_variants(self, value):
        """
        Validate that at least one variant is provided
        """
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one variant is required.")
        
        # Check for duplicate color+size combinations
        combinations = []
        for variant in value:
            color_id = variant.get('color', {}).get('id') if isinstance(variant.get('color'), dict) else variant.get('colour_id')
            size_id = variant.get('size', {}).get('id') if isinstance(variant.get('size'), dict) else variant.get('size_id')
            
            if color_id and size_id:
                combo = f"{color_id}-{size_id}"
                if combo in combinations:
                    raise serializers.ValidationError(
                        f"Duplicate variant combination: Color ID {color_id} and Size ID {size_id} cannot be used twice."
                    )
                combinations.append(combo)
        
        return value
    
    def create(self, validated_data):
        """
        Create Product with multiple variants
        """
        variants_data = validated_data.pop('variants', [])
        
        # Create product
        product = Product.objects.create(**validated_data)
        
        # Create variants
        self._create_variants(product, variants_data)
        
        return product
    
    def update(self, instance, validated_data):
        """
        Update Product and its variants
        """
        variants_data = validated_data.pop('variants', None)
        
        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update variants if provided
        if variants_data is not None:
            self._update_variants(instance, variants_data)
        
        return instance
    
    def _create_variants(self, product, variants_data):
        """
        Helper method to create variants
        """
        for variant_data in variants_data:
            # Generate SKU
            sku = self._generate_sku(product, variant_data)
            
            # Create variant
            ProductVariant.objects.create(
                product=product,
                sku=sku,
                **variant_data
            )
    
    def _update_variants(self, product, variants_data):
        """
        Helper method to update variants
        Handles create, update, delete operations
        """
        existing_variants = {v.id: v for v in product.variants.all()}
        processed_ids = set()
        
        for variant_data in variants_data:
            variant_id = variant_data.get('id')
            
            if variant_id and variant_id in existing_variants:
                # Update existing variant
                variant = existing_variants[variant_id]
                for attr, value in variant_data.items():
                    if attr not in ['id', 'sku']:  # Don't update id or sku
                        setattr(variant, attr, value)
                variant.save()
                processed_ids.add(variant_id)
            else:
                # Create new variant
                # Generate SKU
                sku = self._generate_sku(product, variant_data)
                
                ProductVariant.objects.create(
                    product=product,
                    sku=sku,
                    **variant_data
                )
        
        # Delete variants that weren't in the update data
        for variant_id, variant in existing_variants.items():
            if variant_id not in processed_ids:
                variant.delete()
    
    def _generate_sku(self, product, variant_data):
        """
        Generate SKU for variant
        Format: {product_code}-{color_code}-{size_code}
        """
        color = variant_data.get('color', {})
        if isinstance(color, dict):
            color_code = color.get('code', '')[:3]
        else:
            color_code = str(variant_data.get('colour_id', ''))[:3]
        
        size = variant_data.get('size', {})
        if isinstance(size, dict):
            size_code = size.get('code', '')[:3]
        else:
            size_code = str(variant_data.get('size_id', ''))[:3]
        
        # Generate base SKU
        base_sku = f"{product.code}-{color_code}-{size_code}".upper()
        
        # Ensure uniqueness
        counter = 1
        sku = base_sku
        while ProductVariant.objects.filter(sku=sku).exists():
            sku = f"{base_sku}-{counter}"
            counter += 1
        
        return sku