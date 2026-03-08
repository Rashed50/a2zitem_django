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
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.category import Category
from apps.product.models.product import Product
from apps.product.models.product import ProductImage

##? Serializers Import
from apis.v1.common.user.serializers import UserMiniListSerializer
from apis.v1.attributes.serializers.brandSerializer import MiniBrandSerializer
from apis.v1.attributes.serializers.categorySerializer import MiniCategorySerializer


##TODO:- Serializers Initialization
class ItemSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    category   = MiniCategorySerializer(read_only=True)
    brand      = MiniBrandSerializer(read_only=True)
    
    class Meta:
        model  = Product
        fields = [
            'id', 'slug', 'code',
            
            'name',
            'title',
            'category', 'category_id',
            'brand', 'brand_id',
            'is_active', 
            
            'created_at', 'updated_at', 'created_by', 'updated_by'
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
                'required': True, 
                'allow_null': False,
                'allow_blank': False,
                'error_messages': get_field_error_messages('Title', 'CharField')
            },
        }


