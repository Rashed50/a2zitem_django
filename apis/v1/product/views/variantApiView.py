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

##? Utils Import 
from apis.utils.apiResponse import * 
from apis.utils.pagination import CustomPageNumberPagination, get_paginated_response 
from apis.utils.apiPermission import HasPermission

##? Service Import 
from apis.v1.product.services import queries, filters

##? Model Import 
User = get_user_model() 
from apps.product.models.product import Product
from apps.product.models.variant import ProductVariant

##? Serializer Import 
from apis.v1.product.serializers.productSerializer import ProductSerializer
from apis.v1.product.serializers.variantSerializer import VariantMiniListSerializer

"""
##TODO:- Product Variant Mini List API Views
##* List API Views (GET)
"""
class ProductVariantMiniListAPIView(generics.ListAPIView): 
    authentication_classes = [JWTAuthentication] 
    serializer_class       = VariantMiniListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self): 
        queryset = ProductVariant.objects\
            .filter(product__is_deleted=False, product__is_active=True)\
            .order_by('sku')
        ##? Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(sku__icontains=search)
                | Q(product__code__icontains=search)
                | Q(product__name__icontains=search)
                | Q(product__title__icontains=search)
            )
        else:
            queryset = queryset.none()
        return queryset
    
    def list(self, request, *args, **kwargs): 
        queryset = self.filter_queryset(self.get_queryset())
        response_data = get_paginated_response(
            queryset   = queryset,
            request    = request,
            pagination = 0,
            serializer_class = self.get_serializer
        )
        return response_list(response_data, item_name="Product Variant")
    



