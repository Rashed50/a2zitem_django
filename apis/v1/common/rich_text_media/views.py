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
from core.models.file_model import RichTextEditorMediaFile

##? Serializers Import
from apis.v1.common.rich_text_media.serializers import RichTextEditorMediaSerializer


"""
##! RichTextEditorMedia APIs
##* List, Create
"""
class RichTextEditorMediaListCreateAPIView(generics.ListCreateAPIView):
    queryset           = RichTextEditorMediaFile.objects.all()
    serializer_class   = RichTextEditorMediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class   = CustomPageNumberPagination  
    
    ##? Filtering & Searching
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields   = []   # Fields for ?search = ??
    ordering_fields = []   # Fields for ?ordering = ??
    
    def get_queryset(self):
        queryset = super().get_queryset()

        # Query params [GET /api/media/?content_type=events.event&object_id=1]
        content_type_param = self.request.query_params.get("content_type")
        object_id_param    = self.request.query_params.get("object_id")

        # Filter by content_type if provided
        if content_type_param:
            try:
                app_label, model = content_type_param.split(".")
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                queryset = queryset.filter(content_type=content_type)
            except ContentType.DoesNotExist:
                queryset = queryset.none()  # Invalid content_type

        # Filter by object_id if provided
        if object_id_param:
            queryset = queryset.filter(object_id=object_id_param)

        return queryset
    
    ##! List (GET)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        ##! Disable pagination if pagination= 0 or '0' is in query params
        if request.query_params.get('pagination') in (0, '0', 'false', 'False'):
            response_data = get_paginated_response(
                queryset   = queryset,
                request    = request,
                pagination = 0,
                serializer_class = self.get_serializer
            )
            return response_list(response_data, item_name="Rich Text Editor Media")
            
        ##! For paginated response 
        response_data = get_paginated_response(
            queryset = queryset,
            request  = request,
            serializer_class = self.get_serializer
        )
        return response_list(response_data, item_name="Rich Text Editor Media")
    
    ##! Create (POST)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response_create(serializer.data, item_name='Rich Text Editor Media')
            
    
    
"""
##! RichTextEditorMedia APIs
##* Details, Update, Delete (GET/PUT/PATCH/DELETE)
"""
class RichTextEditorMediaUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = RichTextEditorMediaFile.objects.all()
    serializer_class   = RichTextEditorMediaSerializer
    lookup_field       = 'id'  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    ##! Details (GET)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response_details(serializer.data, item_name="Rich Text Editor Media")
    
    
    ##! Update (PUT/PATCH)
    def update(self, request, *args, **kwargs):
        partial    = kwargs.pop('partial', False)
        instance   = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response_update(serializer.data, serializer=serializer, item_name="Rich Text Editor Media")
             
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


    ##! Delete (DELETE)
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return response_delete(
                item      = instance,
                item_name = "Rich Text Editor Media",  # Or self.serializer_class.Meta.model.__name__.lower()
                request   = request,
            )
        except ProtectedError as e:
            return response_error(error=e, message="Cannot delete this item, it's referenced by other records.")
        except Exception as e:
            return response_error(error=str(e), message="An error occurred while deleting the item.")
