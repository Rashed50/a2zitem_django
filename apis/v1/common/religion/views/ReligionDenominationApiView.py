from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status, generics
from rest_framework import permissions

##? Utils Import
from apis.utils.apiResponse import *
from apis.utils.pagination import CustomPageNumberPagination, get_paginated_response

##? Models Import
from core.models.religion_model import Religion, ReligionDenomination

##? Serializers Import
from apis.v1.common.religion.serializers.ReligionSerializer import ReligionSerializer
from apis.v1.common.religion.serializers.ReligionDenominationSerializer import ReligionDenominationSerializer


"""
##! Religion APIs
##* List, Create
"""
class ReligionDenominationListAPIView(generics.ListAPIView):
    queryset           = ReligionDenomination.objects.all()
    serializer_class   = ReligionDenominationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class   = CustomPageNumberPagination
    
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['religion']                   ## ?religion=1
    search_fields      = ['name', 'religion__name']     ## ?search=...
    ordering_fields    = ['name', 'religion__name']     ## ?ordering=...
    ordering           = ['name'] 
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset
    
    ##! List (GET)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response_data = get_paginated_response(
            queryset   = queryset,
            request    = request,
            pagination = 0,
            serializer_class = self.get_serializer
        )
        return response_list(response_data, item_name="Religion Denomination")