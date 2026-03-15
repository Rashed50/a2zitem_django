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

##? Serializers Import
from apis.v1.common.user.serializers import UserMiniListSerializer



##TODO:- Serializers Initialization
class BrandSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    class Meta:
        model  = Brand
        fields = ['id', 'name', 'logo', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
        read_only_fields = ['id', 'created_by', 'updated_by']
        extra_kwargs = {
            'name' : {
                'required': True, 
                'allow_null': False,
                'allow_blank': False,
                'error_messages': get_field_error_messages('Name', 'CharField')
            },
            # 'logo' : {
            #     'required': False, 
            #     'allow_null': False,
            #     'error_messages': get_field_error_messages('Logo', 'ImageField')
            # },
        }


class MiniBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Brand
        fields = ['id', 'name', 'logo']

