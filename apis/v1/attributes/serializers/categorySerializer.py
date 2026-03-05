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

class MiniCategorySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source  = 'created_by.name',
        read_only = True
    )
    class Meta:
        model  = Category
        fields = ["id", "slug", "name", "created_at", "created_by"]

##TODO:- Serializers Initialization
class CategoryTreeSerializer(serializers.ModelSerializer):
    created_by = UserMiniListSerializer(read_only=True)
    updated_by = UserMiniListSerializer(read_only=True)
    parent     = MiniCategorySerializer(read_only=True)
    parent_id  = serializers.PrimaryKeyRelatedField(
            queryset   = Category.objects.all(),
            # source     = 'parent',
            write_only = True,
            required   = False,
            allow_null = True,
            error_messages = get_field_error_messages('Parent', 'PrimaryKeyRelated'),
        )

    class Meta:
        model  = Category
        fields = [
            'id',
            'slug',
            'name',
            'parent',
            'parent_id',
            # 'children',
            'logo',
            'is_active',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
        extra_kwargs = {
            'name': {
                'required'       : True,
                'allow_blank'    : False,
                'error_messages' : get_field_error_messages('Name', 'CharField')
            },
        }
        
    def validate_parent(self, value):
        if self.instance:
            if value == self.instance:
                raise serializers.ValidationError("Category cannot be its own parent.")
            if value and value in self.instance.get_descendants():
                raise serializers.ValidationError("Cannot assign child as parent.")
        return value

    def create(self, validated_data):
        request  = self.context['request']
        parent   = validated_data.pop('parent_id', None)
        category = Category.objects.create(parent=parent, **validated_data)
        return category
    
    def update(self, instance, validated_data):
        request  = self.context['request']
        parent   = validated_data.pop('parent_id', None)
        instance = super().update(instance, validated_data)
        if parent is not None:
            instance.parent = parent
            instance.save()
        return instance



class CategoryDetailsTreeSerializer(serializers.ModelSerializer):
    created_by     = UserMiniListSerializer(read_only=True)
    updated_by     = UserMiniListSerializer(read_only=True)
    parent         = MiniCategorySerializer(read_only=True)
    parent_chain   = serializers.SerializerMethodField()
    children_chain = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = [
            'id',
            'slug',
            'name',
            'logo',
            'is_active',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            
            ##? Tree
            'parent', 'parent_chain',
            'children_chain',
        ]
    
    def get_parent_chain(self, obj):
        ancestors = obj.get_ancestors(include_self=False)
        # return [{"id": cat.id, "slug": cat.slug, "name": cat.name} for cat in ancestors]
        return MiniCategorySerializer(ancestors, many=True, context=self.context).data
        
    def get_children_chain(self, obj):
        children = obj.get_children()
        # return [{"id": cat.id, "slug": cat.slug, "name": cat.name} for cat in children]
        return MiniCategorySerializer(children, many=True, context=self.context).data
        
