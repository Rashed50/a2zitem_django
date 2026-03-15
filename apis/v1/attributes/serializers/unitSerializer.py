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
from apps.product.models.unit import UnitOfMeasure

##? Serializers Import
from apis.v1.common.user.serializers import UserMiniListSerializer



##TODO:- Serializers Initialization
class UnitOfMeasureSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    class Meta:
        model  = UnitOfMeasure
        fields = ['id', 'name', 'symbol', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by']
        read_only_fields = ['id', 'created_by', 'updated_by']
        extra_kwargs = {
            'name' : {
                'required': True, 
                'allow_null': False,
                'allow_blank': False,
                'error_messages': get_field_error_messages('Name', 'CharField')
            },
            'symbol' : {
                'required': False, 
                'allow_null': True,
                'allow_blank': True,
                'error_messages': get_field_error_messages('Symbolic Name', 'CharField')
            },
        }


class MiniUnitOfMeasureSerializer(UnitOfMeasureSerializer):
    class Meta(UnitOfMeasureSerializer.Meta):
        fields = ['id', 'name', 'symbol']