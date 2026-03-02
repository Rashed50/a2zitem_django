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
#from apis.utils.apiResponse import * 
#from apis.utils.pagination import CustomPageNumberPagination, get_paginated_response 

##? Service Import 
#ffrom apis.inbound.service import query, filtering, searching, permissions 

##? Model Import 
User = get_user_model() 

#from apps.purchase.models import YourModel, RelatedModel 

##? Serializer Import 
#from apis.v1.purchase.serializers.purchase import PurchaseSerializer 


##! Create API Views (POST) 
#class YourCreateAPIView(generics.CreateAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    serializer_class       = YourModelSerializer 

#    def get_queryset(self): 
#        queryset = super().get_queryset() 
#        return queryset 

#    def perform_create(self, serializer): 
#        serializer.save(created_by=self.request.user) 


#    def create(self, request, *args, **kwargs): 
#        try: 
#            serializer = self.get_serializer(data=request.data) 
#            if serializer.is_valid(): 
#                self.perform_create(serializer) 
#                return response_create(serializer.data, item_name='YourModel') 
#            else: 
#                return response_error(serializer.errors, status=400, message='Validation failed') 
#        except IntegrityError as e: 
#            return response_error(e, status=400, message='Database integrity error') 
#        except Exception as e: 
#            return response_error(e, status=500, message='Internal server error') 



##! List API View (GET) 
#class YourListAPIView(generics.ListAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    pagination_class       = CustomPageNumberPagination 
#    serializer_class       = YourModelSerializer 

#    def get_queryset(self): 
#        queryset = query.YourModelData() 
#        ##? Filtering 
#        status     = self.request.GET.get('status', 'active') 
#        start_date = self.request.GET.get('startDate', None) 
#        end_date   = self.request.GET.get('endDate', None) 
#        unit_id    = self.request.GET.get('unit_id', None) 
#        filter_service = filtering.YourFilterService( 
#            status     = status, 
#            start_date = start_date, 
#            end_date   = end_date, 
#            unit_id    = unit_id, 
#        ) 
#        queryset = filter_service.apply_filter(queryset) 
#        ##? Searching 
#        search = self.request.GET.get('search', None) 
#        if search: 
#            search_service = searching.YourSearchService(search) 
#            queryset = search_service.apply_search(queryset) 
#        return queryset 

#    def list(self, request, *args, **kwargs): 
#        queryset = self.filter_queryset(self.get_queryset()) 
#        ##? Disable pagination if pagination= 0 or '0' is in query params 
#        if request.query_params.get('pagination') in (0, '0', 'false', 'False'): 
#            response_data = get_paginated_response( 
#                queryset   = queryset, 
#                request    = request, 
#                pagination = 0, 
#                serializer_class = self.get_serializer 
#            ) 
#            return response_list(response_data, item_name='YourModel') 
#        ##? For paginated response  
#        else: 
#            response_data = get_paginated_response( 
#                queryset = queryset, 
#                request  = request, 
#                serializer_class = self.get_serializer 
#            ) 
#            return response_list(response_data, item_name='YourModel') 

##! Detail API View (GET) 
#class YourDetailAPIView(generics.RetrieveAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    serializer_class       = YourModelSerializer 
#    lookup_field           = 'id' 

#    lookup_url_kwarg       = 'id' 
#    def get_queryset(self): 
#        queryset = query.YourModelData() 
#        return queryset 

#    def retrieve(self, request, *args, **kwargs): 
#        try: 
#            instance = self.get_object() 
#            serializer = self.get_serializer(instance) 
#            return response_details(serializer.data, item_name='YourModel') 
#        except Exception as e: 
#            return response_error(e, status=400, message='Something went wrong') 

##! Update API View (PUT/PATCH) 
#class YourUpdateAPIView(generics.UpdateAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    serializer_class       = YourModelSerializer 
#    lookup_field           = 'id' 

#    lookup_url_kwarg       = 'id' 
#    def get_queryset(self): 
#        queryset = query.YourModelData() 
#        return queryset 

#    def update(self, request, *args, **kwargs): 
#        partial    = kwargs.pop('partial', False) 
#        try: 
#            instance = self.get_object() 
#            serializer = self.get_serializer(instance, data=request.data, partial=partial) 
#            #serializer.is_valid(raise_exception=True) 
#            if serializer.is_valid(): 
#                self.perform_update(serializer) 
#                return response_update(serializer.data, serializer=serializer, item_name='YourModel') 
#            else: 
#                return response_error(serializer.errors, status=400, message='Validation failed') 
#        except IntegrityError as e: 
#            return response_error(str(e), status=400, message='Database integrity error') 
#        except Exception as e: 
#            return response_error(str(e), status=500, message='Internal server error') 

#def partial_update(self, request, *args, **kwargs): 
#    kwargs['partial'] = True 
#    return self.update(request, *args, **kwargs) 
##! Delete API View (DELETE) 
#class YourDeleteAPIView(generics.DestroyAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    lookup_field           = 'id' 

#    lookup_url_kwarg       = 'id' 
#    def get_queryset(self): 
#        queryset = query.YourModelData() 
#        return queryset 

#    def destroy(self, request, *args, **kwargs): 
#        try: 
#            instance = self.get_object() 
#            self.perform_destroy(instance) 
#            return response_delete(item=instance, item_name='YourModel', request=request,) 
#        except IntegrityError as e: 
#            return response_error(str(e), status=400, message='Database integrity error') 
#        except Exception as e: 
#            return response_error(str(e), status=400, message='Something went wrong') 

##! Combined Create and List API View 
#class YourListCreateAPIView(generics.ListCreateAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    serializer_class       = YourModelSerializer 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    pagination_class       = CustomPageNumberPagination 
#    http_method_names      = ['get', 'post'] 

#    filter_backends  = [SearchFilter, OrderingFilter, DjangoFilterBackend] 
#    ordering_fields  = ['id', 'name'] 
#    search_fields    = ['name'] 
#    filterset_fields = { 
#        'status__name' : ['exact', 'icontains'], 
#        'created_at'   : ['gte', 'lte'], 
#        'updated_at'   : ['gte', 'lte'], 
#        'deleted_at'   : ['isnull'], 
#        'id'           : ['exact'], 
#        'name'         : ['exact', 'icontains'], 
#        'email'        : ['exact', 'icontains'], 
#        'phone'        : ['exact', 'icontains'], 
#        'address__zip_code__id' : ['in'], 
#    } 

#    def get_queryset(self): 
#        #queryset = super().get_queryset() 
#        queryset = query.YourModelData() 
#        return queryset 

#    ##? Create (POST) 
#    def create(self, request, *args, **kwargs): 
#        try: 
#            serializer = self.get_serializer(data=request.data) 
#            if serializer.is_valid(): 
#                self.perform_create(serializer) 
#                return response_create(serializer.data, item_name='YourModel') 
#            else: 
#                return response_error(serializer.errors, status=400, message='Validation failed') 
#        except IntegrityError as e: 
#            return response_error(str(e), status=400, message='Database integrity error') 
#        except Exception as e: 
#            return response_error(str(e), status=500, message='Something went wrong') 

#    ##? List (GET) 
#    def list(self, request, *args, **kwargs): 
#        queryset = self.filter_queryset(self.get_queryset()) 
#        ##? Disable pagination if pagination= 0 or '0' is in query params 
#        if request.query_params.get('pagination') in (0, '0', 'false', 'False'): 
#            response_data = get_paginated_response( 
#                queryset   = queryset, 
#                request    = request, 
#                pagination = 0, 
#                serializer_class = self.get_serializer 
#            ) 
#            return response_list(response_data, item_name='YourModel') 

#        ##! For paginated response 
#        response_data = get_paginated_response( 
#            queryset = queryset, 
#            request  = request, 
#            serializer_class = self.get_serializer 
#        ) 
#        return response_list(response_data, item_name='YourModel') 

##! Combined  Details, Update, Delete (GET/PUT/PATCH/DELETE) API View 
#class YourRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): 
#    queryset = YourModel.objects.all().order_by('id') 
#    serializer_class       = YourModelSerializer 
#    authentication_classes = [JWTAuthentication] 
#    permission_classes     = [IsAuthenticatedOrReadOnly] 
#    lookup_field           = 'id' 
#    lookup_url_kwarg       = 'id' 
#    http_method_names      = ['get', 'put', 'patch', 'delete'] 

#    ##? Details (GET) 
#    def retrieve(self, request, *args, **kwargs): 
#        try: 
#            instance = self.get_object() 
#            serializer = self.get_serializer(instance) 
#            return response_details(serializer.data, item_name='YourModel') 
#        except Exception as e: 
#            return response_error(str(e), status=500, message='Something went wrong') 

#    ##? Update (PUT/PATCH) 
#    def update(self, request, *args, **kwargs): 
#        partial    = kwargs.pop('partial', False) 
#        try: 
#            instance = self.get_object() 
#            serializer = self.get_serializer(instance, data=request.data, partial=partial) 
#            if serializer.is_valid(): 
#                self.perform_update(serializer) 
#                return response_update(serializer.data, serializer=serializer, item_name='YourModel') 
#            else: 
#                return response_error(serializer.errors, status=400, message='Validation failed') 
#        except IntegrityError as e: 
#            return response_error(str(e), status=400, message='Database integrity error') 
#        except Exception as e: 
#            return response_error(str(e), status=500, message='Something went wrong') 

#    def partial_update(self, request, *args, **kwargs): 
#        kwargs['partial'] = True 
#        return self.update(request, *args, **kwargs) 

#    ##? Delete (DELETE) 
#    def destroy(self, request, *args, **kwargs): 
#        try: 
#            instance = self.get_object() 
#            self.perform_destroy(instance) 
#            return response_delete( 
#                item      = instance, 
#                item_name = 'Brand',  # Or self.serializer_class.Meta.model.__name__.lower() 
#                request   = request, 
#            ) 
#        except ProtectedError as e: 
#            return response_error(error=e, message="Cannot delete this item, it's referenced by other records.") 
#        except Exception as e: 
#            return response_error(error=str(e), message="An error occurred while deleting the item.") 

