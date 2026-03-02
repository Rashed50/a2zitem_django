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
from apps.product.models.category import Category

##? Serializers Import
from apis.v1.common.user.serializers import UserMiniListSerializer



##TODO:- Serializers Initialization
class CategorySerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    
    ## 👉 Parent শুধু ID হিসেবে নিবে
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    ## 👉 Children nested ভাবে দেখাবে
    children = serializers.SerializerMethodField()
    
    class Meta:
        model  = Category
        fields = [
            'id',
            'slug',
            'name',
            'logo',
            'parent',
            'children',
            'created_by',
            'updated_by',
        ]
        read_only_fields = ['id', 'slug', 'created_by', 'updated_by', 'children']
        extra_kwargs = {
            'name' : {
                'required': True, 
                'allow_null': False,
                'allow_blank': False,
                'error_messages': get_field_error_messages('Name', 'CharField')
            },
        }
        
    def get_children(self, obj):
        children = obj.get_children()
        if children:
            return CategorySerializer(children, many=True, context=self.context).data
        return []

    def validate_parent(self, value):
        if self.instance:
            if value == self.instance:
                raise serializers.ValidationError("Category cannot be its own parent.")
            if value and value in self.instance.get_descendants():
                raise serializers.ValidationError("Cannot assign a child as parent.")
        return value


