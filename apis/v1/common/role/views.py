from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication 

from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend

##? Utils Import
from apis.utils.apiResponse import *
from apis.utils.pagination import CustomPageNumberPagination, get_paginated_response 
from apis.v1.common.permission.constants import ALLOWED_PERMISSION_MODELS
from apis.utils.apiPermission import HasPermission

##? Models Import
from django.contrib.auth.models import Group

##? Serializers Import
from apis.v1.common.role.serializers import GroupSerializer, GroupListSerializer

"""
##TODO:- Group/Role API
##* List/Create API Views (GET,POST)
"""
class GroupListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication] 
    queryset = Group.objects.prefetch_related("permissions")
    serializer_class   = GroupSerializer
    permission_classes = [HasPermission]
    
    # search, filter, ordering
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields   = ['name']
    ordering_fields = ['name']

    def get_permissions(self):
        if self.request.method == "POST":
            self.required_perms = ["auth.add_group"]
        else:
            self.required_perms = ["auth.view_group"]
        return super().get_permissions()
    
    def get_serializer_class(self): 
        if self.request.method == 'POST':
            return GroupSerializer
        return GroupListSerializer
    
    # permission_classes = [IsModeratorUser] 
    # def get_permissions(self):
    #     permission = IsModeratorUser()
    #     if self.request.method == "POST":
    #         permission.required_perms = ["events.add_event"]
    #         permission.allowed_groups  = ["Admin", "Moderator"]
    #     elif self.request.method == "GET":
    #         permission.required_perms = ["events.view_event"]
    #         permission.allowed_groups  = ["Admin", "Moderator", "User"]
    #     return [permission]
    
    def list(self, request, *args, **kwargs):
        # queryset   = self.get_queryset()
        # serializer = self.get_serializer(queryset, many=True)
        # return response_list(serializer.data, item_name="Role/Group")
        queryset = self.filter_queryset(self.get_queryset())
        ##! For paginated response 
        response_data = get_paginated_response(
            queryset = queryset,
            request  = request,
            serializer_class = self.get_serializer_class()
        )
        return response_list(response_data, item_name="Roles/Groups")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        return response_create(
            GroupSerializer(group).data,
            item_name="Role/Group"
        )
        
        
"""
##TODO:- Group/Role API
##* Details/Update/Delete API Views (GET,PUT,PATCH,DELETE)
"""
class GroupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication] 
    queryset           = Group.objects.all().order_by('id') 
    serializer_class   = GroupSerializer 
    lookup_field       = 'id'
    lookup_url_kwarg   = 'id'
    permission_classes = [HasPermission]
    
    def get_permissions(self):
        if self.request.method == "PUT":
            self.required_perms = ["auth.change_group"]
        elif self.request.method == "PATCH":
            self.required_perms = ["auth.change_group"]
        elif self.request.method == "DELETE":
            self.required_perms = ["auth.delete_group"]
        elif self.request.method == "GET":
            self.required_perms = ["auth.view_group"]
        return super().get_permissions()
    
    # permission_classes = [IsAdminUser]
    # def get_permissions(self):
    #     permission = IsAdminUser()
    #     if self.request.method == "PUT":
    #         permission.required_perms = ["events.change_event"]
    #         permission.allowed_groups  = ["Admin", "Moderator"]
    #     elif self.request.method == "PATCH":
    #         permission.required_perms = ["events.change_event"]
    #         permission.allowed_groups  = ["Admin", "Moderator"]
    #     elif self.request.method == "DELETE":
    #         permission.required_perms = ["events.delete_event"]
    #         permission.allowed_groups  = ["Admin", "Moderator"]
    #     elif self.request.method == "GET":
    #         permission.required_perms = ["events.view_event"]
    #         permission.allowed_groups  = ["Admin", "Moderator", "User"]
    #     return [permission]
    
    ##! Retrieve/Details
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_details(serializer.data, item_name='Group/Role')
    
    ##! Update
    def update(self, request, *args, **kwargs): 
        partial = kwargs.pop('partial', False) 
        instance = self.get_object() 
        serializer = self.get_serializer(instance, data=request.data, partial=partial) 
        serializer.is_valid(raise_exception=True) 
        self.perform_update(serializer) 
        return response_update(serializer.data, serializer=serializer, item_name='Group/Role')
    
    ##! Delete
    def destroy(self, request, *args, **kwargs): 
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return response_delete(item=instance, item_name='Group/Role', request=request)
        


