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
from rest_framework.parsers import MultiPartParser, FormParser

##? Utils Import 
from apis.utils.apiResponse import * 
from apis.utils.pagination import CustomPageNumberPagination, get_paginated_response 
from apis.utils.apiPermission import HasPermission

##? Service Import 
from apis.v1.product.services import queries, filters

##? Model Import 
User = get_user_model() 
from apps.product.models.product import Product, ProductImage

##? Serializer Import
from apis.v1.product.serializers.productSerializer import ProductSerializer, ProductImageSerializer


##! ===================== [ For Admin ] =====================
"""
##TODO:- Product Item Create & List API Views
##* List/Create API Views (GET,POST)
"""
class ProductListCreateAPIView(generics.ListCreateAPIView): 
    authentication_classes = [JWTAuthentication] 
    pagination_class       = CustomPageNumberPagination 
    serializer_class       = ProductSerializer
    
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering        = ['name']  
    
    ##? Permission 
    permission_classes = [HasPermission] 
    permission_policy  = {"GET":{"admin": True}, "POST":{"admin":True}}
    def get_permissions(self):
        if self.request.method == "POST":
            self.required_perms = ["product.add_product"]
        else:
            self.required_perms = ["product.view_product"]
        return super().get_permissions() 
    
    ##? Queryset
    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        
        ##? Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) 
                | Q(title__icontains=search) 
                | Q(code__icontains=search) 
                | Q(description__icontains=search) 
                | Q(brand__name__icontains=search) 
                | Q(category__name__icontains=search) 
            ).distinct()
        return queryset
    
    ##! Create
    def perform_create(self, serializer): 
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response_create(serializer.data,item_name="Item") 

    ##! List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response_data = get_paginated_response(
            queryset = queryset,
            request  = request,
            serializer_class = self.get_serializer
        )
        return response_list(response_data, item_name="Item")




"""
##TODO:- Item Retrieve, Update, Destroy API Views
##* Details/Update/Delete API Views (GET,PUT,PATCH,DELETE)
"""
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): 
    authentication_classes = [JWTAuthentication] 
    serializer_class       = ProductSerializer
    
    ##? Permission 
    permission_classes = [HasPermission] 
    permission_policy  = {"GET":{"admin": True}, "PUT":{"admin":True}, "PATCH":{"admin":True}, "DELETE":{"admin":True}}
    def get_permissions(self):
        if self.request.method == "PUT":
            self.required_perms = ["product.change_Item"]
        elif self.request.method == "PATCH":
            self.required_perms = ["product.change_Item"]
        elif self.request.method == "DELETE":
            self.required_perms = ["product.delete_Item"]
        else:
            self.required_perms = ["product.view_Item"]
        return super().get_permissions()
    
    ##? Queryset
    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        return queryset
    
    ##! Retrieve
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_details(serializer.data, item_name="Item")
    
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
        return response_update(serializer.data, serializer=serializer, item_name='Item')
    
    ##! Destroy
    # def perform_destroy(self, instance):
    #     with transaction.atomic():
    #         instance.delete()
    def destroy(self, request, *args, **kwargs): 
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return response_delete(item=instance, item_name='Item', request=request)


"""
##TODO:- Product Image Create
##* Create API Views (POST)
"""

class ProductImageCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [HasPermission]
    parser_classes         = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method == "POST":
            self.required_perms = ["product.add_productimage"]
        else:
            self.required_perms = ["product.view_product"]
        return super().get_permissions()
    
    def post(self, request, format=None):
        product_id = request.data.get('product')
        images     = request.FILES.getlist('images')  
        
        if not product_id:
            return Response({
                "error": "Product ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not images:
            return Response({
                "error": "At least one image is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                "error": f"Product with id {product_id} does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        
        created_images = []
        for image in images:
            product_image = ProductImage.objects.create(
                product=product,
                image=image,
                alt_text=request.data.get('alt_text', '')  
            )
            created_images.append(product_image)
        
        serializer = ProductImageSerializer(created_images, many=True)
        return Response({
            "message": f"Successfully created {len(created_images)} image(s)",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class ProductImageDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [HasPermission]
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            self.required_perms = ["product.delete_productimage"]
        else:
            self.required_perms = ["product.view_product"]
        return super().get_permissions()
    
    def delete(self, request, pk):
        try:
            product_image = ProductImage.objects.get(id=pk)
        except ProductImage.DoesNotExist:
            return Response({"error": "Product image not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product_image.delete()
        return Response({"message": "Product image deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

##! ================ [ For Customer ] ================
class CusomerProductListAPIView(generics.ListAPIView): 
    authentication_classes = [] 
    permission_classes     = [permissions.AllowAny]
    pagination_class       = CustomPageNumberPagination 
    serializer_class       = ProductSerializer
    
    ##? Queryset
    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        
        ##? Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) 
                | Q(title__icontains=search) 
                | Q(code__icontains=search) 
            ).distinct()
        return queryset
    
    ##! List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response_data = get_paginated_response(
            queryset = queryset,
            request  = request,
            serializer_class = self.get_serializer
        )
        return response_list(response_data, item_name="Item")
    
class CustomerProductDetailsAPIView(generics.RetrieveAPIView): 
    authentication_classes = [] 
    permission_classes     = [permissions.AllowAny]
    serializer_class       = ProductSerializer
    
    ##? Queryset
    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        return queryset
    
    ##! Retrieve
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_details(serializer.data, item_name="Item")