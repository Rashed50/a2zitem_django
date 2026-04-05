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

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductImage
        fields = [
            'id',
            'image',
        ]

##TODO:- Serializers Initialization
class ProductSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    category   = MiniCategorySerializer(read_only=True)
    brand      = MiniBrandSerializer(read_only=True)
    images     = ProductImageSerializer(many=True, read_only=True)
    
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
            'images',
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

    ##? ============= [ Validations ] ============= ##
    def validate_name(self, value):
        qs = Product.objects.filter(name=value)
        if self.instance:  
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Product with this Item Name already exists.")
        return value
    
    def validate_title(self, value):
        """Auto-set title from name if not provided"""
        if not value and self.initial_data.get('name'):
            return self.initial_data.get('name')
        return value
    
    def validate_variants(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one variant is required.")
        
        # combinations = []
        # for variant in value:
        #     color_id = self._extract_id(variant, 'color')
        #     size_id  = self._extract_id(variant, 'size')
            
        #     if not color_id or not size_id:
        #         raise serializers.ValidationError(
        #             "Each variant must have both a color and a size."
        #         )
            
        #     combo = f"{color_id}-{size_id}"
        #     if combo in combinations:
        #         raise serializers.ValidationError(
        #             f"Duplicate color and size combination found: Color {color_id}, Size {size_id}"
        #         )
        #     combinations.append(combo)
        
        return value

    ##? ============= [ Create & Update ] ============= ##
    
    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        ## Create product
        product = Product.objects.create(**validated_data)
        ## Create variants
        self._create_variants(product, variants_data)
        return product
    
    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)
        
        ## Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        ## Update variants if provided
        if variants_data is not None:
            self._update_variants(instance, variants_data)
        
        return instance
    
    def _create_variants(self, product, variants_data):
        for variant_data in variants_data:
            ProductVariant.objects.create(product = product,**variant_data)
            
    def _update_variants(self, product, variants_data):
        existing_variants = {v.id: v for v in product.variants.all()}
        processed_ids     = set()

        for variant_data in variants_data:
            variant_id = variant_data.get("id")
            if "color" in variant_data and variant_data["color"]:
                new_color_id = getattr(variant_data["color"], "id", None)
            else:
                new_color_id = variant_data.get("color_id")

            if "size" in variant_data and variant_data["size"]:
                new_size_id = getattr(variant_data["size"], "id", None)
            else:
                new_size_id = variant_data.get("size_id")

            if "unit" in variant_data and variant_data["unit"]:
                new_unit_id = getattr(variant_data["unit"], "id", None)
            else:
                new_unit_id = variant_data.get("unit_id")

            ##? Duplicate check
            duplicate_qs = ProductVariant.objects.filter(
                product  = product,
                color_id = new_color_id,
                size_id  = new_size_id
            )
            if variant_id:
                duplicate_qs = duplicate_qs.exclude(id=variant_id)

            if duplicate_qs.exists():
                raise serializers.ValidationError(
                    # f"Variant with color ID {new_color_id} and size ID {new_size_id} already exists for this product."
                    "Variant with color and size already exists for this product."
                )

            if variant_id and variant_id in existing_variants:
                ##? Update existing variant
                variant = existing_variants[variant_id]
                for attr, value in variant_data.items():
                    if attr not in ["id", "sku"]:
                        setattr(variant, attr, value)
                variant.save()
                processed_ids.add(variant_id)
            else:
                ##? Create New Variant
                variant = ProductVariant.objects.create(
                    product  = product,
                    color_id = new_color_id,
                    size_id  = new_size_id,
                    unit_id  = new_unit_id,
                    stock    = variant_data.get("stock", 0),
                    selling_price  = variant_data.get("selling_price", 0),
                    purchase_price = variant_data.get("purchase_price", 0),
                    min_stock      = variant_data.get("min_stock", 0),
                )
                processed_ids.add(variant.id)

        ##? Delete variants removed from frontend
        for variant_id, variant in existing_variants.items():
            if variant_id not in processed_ids:
                variant.delete()
    
    
                
                
# class ProductMiniSerializer(serializers.ModelSerializer):
#     category = MiniCategorySerializer(read_only=True)
#     brand    = MiniBrandSerializer(read_only=True)
#     class Meta:
#         model  = Product
#         fields = [
#             'id', 
#             'slug', 
#             'code',
#             'name',
#             'title',
#             'category',
#             'brand', 
#         ]