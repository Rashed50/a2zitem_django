from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend

##? Utils Import
from apis.utils.apiResponse import *
from apis.utils.apiPermission import HasPermission
from apis.v1.common.permission.constants import ALLOWED_PERMISSION_MODELS

##? Models Import
from django.contrib.auth.models import Permission

##? Serializers Import
from apis.v1.common.permission.serializers import PermissionSerializer

"""
##! Permission APIs
##* List
"""
class PermissionListAPIView(generics.ListAPIView):
    serializer_class   = PermissionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [HasPermission]
    filter_backends    = [SearchFilter, OrderingFilter]

    search_fields   = ["name", "codename"]
    ordering_fields = ["codename", "id"]
    
    def get_permissions(self):
        if self.request.method == "GET":
            self.required_perms = ["auth.view_permission"]
        return super().get_permissions()
    
    def get_queryset(self):
        content_type_filters = []

        for app_label, models in ALLOWED_PERMISSION_MODELS.items():
            content_type_filters.extend(
                ContentType.objects.filter(
                    app_label = app_label,
                    model__in = models
                )
            )

        return Permission.objects.filter(
            content_type__in=content_type_filters
        ).order_by("content_type__app_label", "content_type__model", "codename")
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response_list(serializer.data, item_name="Permission")
            
    