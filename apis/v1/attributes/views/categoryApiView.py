import json, csv, requests, datetime 
from django.http import HttpResponse 
from django.conf import settings 
from django.contrib.auth import get_user_model, get_permission_codename 

from django.db import models, transaction, IntegrityError 
from django.db.models import Q, F, Count, Value, Prefetch 
from django.db.models.functions import Concat 

from django.utils import timezone 
from django.utils.dateformat import format 
from django.utils.timezone import make_aware, localtime 

from rest_framework import status, generics, permissions 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.validators import ValidationError 
from rest_framework.filters import SearchFilter, OrderingFilter 
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django_filters.rest_framework import DjangoFilterBackend 

from mptt.templatetags.mptt_tags import cache_tree_children

##? Utils Import 
from apis.utils.apiResponse import * 
from apis.utils.pagination import CustomPageNumberPagination, get_paginated_response 
from apis.utils.apiPermission import HasPermission

##? Service Import 
# from apis.v1.attributes.services import queries

##? Model Import 
User = get_user_model() 
from apps.product.models.category import Category

##? Serializer Import 
from apis.v1.attributes.serializers.categorySerializer import CategorySerializer



"""
##TODO:- Category Create & List API Views
##* List/Create API Views (GET,POST)
"""
class CategoryListCreateAPIView(generics.ListCreateAPIView): 
    authentication_classes = [JWTAuthentication] 
    pagination_class       = CustomPageNumberPagination 
    serializer_class       = CategorySerializer
    
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering        = ['name']  
    
    ##? Permission 
    permission_classes = [HasPermission] 
    permission_policy  = {"GET":{"admin": True}, "POST":{"admin":True}}
    def get_permissions(self):
        if self.request.method == "POST":
            self.required_perms = ["product.add_color"]
        else:
            self.required_perms = ["product.view_color"]
        return super().get_permissions() 
    
    # ##? Queryset
    def get_queryset(self):
        queryset = Category.objects.all().select_related('parent')
        search   = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(Q(name__icontains=search))

        return queryset
    
    ##! Create
    def perform_create(self, serializer): 
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response_create(serializer.data,item_name="Category") 

    ##! List
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     response_data = get_paginated_response(
    #         queryset = queryset,
    #         request  = request,
    #         serializer_class = self.get_serializer
    #     )
    #     return response_list(response_data, item_name="Category")
    
    def list(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        tree = cache_tree_children(queryset)
        serializer = self.get_serializer(tree, many=True)
        return Response(serializer.data)




"""
##TODO:- Category Retrieve, Update, Destroy API Views
##* Details/Update/Delete API Views (GET,PUT,PATCH,DELETE)
"""
class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Category.objects.all().order_by('name') 
    authentication_classes = [JWTAuthentication] 
    serializer_class       = CategorySerializer
    
    ##? Permission 
    permission_classes = [HasPermission] 
    permission_policy  = {"GET":{"admin": True}, "PUT":{"admin":True}, "PATCH":{"admin":True}, "DELETE":{"admin":True}}
    def get_permissions(self):
        if self.request.method == "PUT":
            self.required_perms = ["product.change_color"]
        elif self.request.method == "PATCH":
            self.required_perms = ["product.change_color"]
        elif self.request.method == "DELETE":
            self.required_perms = ["product.delete_color"]
        else:
            self.required_perms = ["product.view_color"]
        return super().get_permissions()
    
    ##! Retrieve
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_details(serializer.data, item_name="Category")
    
    ##! Update
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    def partial_update(self, request, *args, **kwargs): 
        kwargs['partial'] = True 
        return self.update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs): 
        partial = kwargs.pop('partial', False) 
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=partial) 
        serializer.is_valid(raise_exception=True) 
        self.perform_update(serializer) 
        return response_update(serializer.data, serializer=serializer, item_name='Category')
    
    ##! Destroy
    # def perform_destroy(self, instance):
    #     with transaction.atomic():
    #         instance.delete()
    def destroy(self, request, *args, **kwargs): 
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return response_delete(item=instance, item_name='Category', request=request)

