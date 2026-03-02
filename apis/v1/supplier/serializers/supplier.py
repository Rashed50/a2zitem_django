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
from apps.supplier.models import Supplier

##? Serializers Import
from apis.v1.common.user.serializers import UserMiniListSerializer


##? Serializers Creation
class SupplierSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    
    class Meta:
        model  = Supplier
        fields = [
            ##* Read Only Fields
            'id', 'slug', 'created_at', 'updated_at', 'created_by', 'updated_by', 
            
            ##* Input Fields
            'name', 'contact', 'email', 'phone', 'address', 'is_active', 
        ]
        extra_kwargs = {
            'id'         : {'read_only': True},
            'slug'       : {'read_only': True},
            'created_at' : {'read_only': True},
            'updated_at' : {'read_only': True},
            'name' : {
                    'required': True, 
                    'allow_blank': False, 
                    'error_messages': get_field_error_messages('Company Name', 'Required')
                },
            'contact' : {
                    'required': True, 
                    'allow_null': False,
                    'allow_blank': False, 
                    'error_messages': get_field_error_messages('Contact Person', 'CharField')
                },
            'email' : {
                    'required': False, 
                    'allow_blank': True, 
                    'error_messages': get_field_error_messages('Email', 'EmailField')
                },
            'phone' : {
                    'required': True, 
                    'allow_null': False,
                    'allow_blank': False, 
                    'error_messages': get_field_error_messages('Phone', 'CharField')
                },
            'address' : {
                    'required': False, 
                    'allow_blank': True, 
                    'error_messages': get_field_error_messages('Address', 'CharField')
            },
            'is_active' : {
                    'required': False, 
                    'error_messages': get_field_error_messages('Status', 'BooleanField')
            },
        }
