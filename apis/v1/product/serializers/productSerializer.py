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



##? Serializers Creation

#class StatusSerializer(serializers.ModelSerializer): 
#    class Meta: 
#        model  = Status 
#        fields = ['id', 'name'] 

#class ProductSerializer(serializers.ModelSerializer): 
#     is_active = serializers.BooleanField(write_only=True, required=False, default=False) 

#     status    = StatusSerializer(read_only=True) 
#     status_id = serializers.PrimaryKeyRelatedField( 
#         source     = 'status', 
#         queryset   = Status.objects.all(), 
#         write_only = True, 
#         required   = False, 
#         allow_null = True, 
#         error_messages = get_field_error_messages('Status', 'PrimaryKeyRelated')
#     ) 

#     test_field = TestSerializer(read_only=True, source='test') 
#     test_id    = serializers.PrimaryKeyRelatedField( 
#         source     = 'test', 
#         queryset   = Test.objects.all(), 
#         write_only = True, 
#         required   = False, 
#         allow_null = True, 
#         error_messages = get_field_error_messages('Test (item)', 'PrimaryKeyRelated') 
#     ) 

#     class Meta: 
#         model = YourModel 
#         fields = ['is_active', 'status', 'status_id', 'test_field', 'test_id'] 

#     def validate(self, attrs): 
#         request = self.context.get('request', None) 
#         return attrs 

#     ##! Create 
#     def create(self, validated_data): 
#         request  = self.context.get('request', None) 
#         is_draft = validated_data.pop('is_draft', False) 
#         items_data = validated_data.pop('itemsData', []) 
#         try: 
#             with transaction.atomic(): 
#                 objects = YourModel.objects.create( 
#                     created_by=request.user, 
#                     **validated_data 
#                 ) 
#                 for item_data in items_data: 
#                     YourDetailsModel.objects.create(parent=objects, **item_data) 
#         except Exception as e: 
#             return response_error(str(e), status=500, message='Internal server error') 
#         return objects 

#     ##! Update 
#     def update(self, instance, validated_data): 
#         request  = self.context.get('request', None) 
#         items_data = validated_data.pop('details_model_related_name', []) 

#         # Main fields update 
#         for attr, value in validated_data.items(): 
#             setattr(instance, attr, value) 
#         instance.save() 

#         # Handle items 
#         existing_items = {item.id: item for item in instance.details_model_related_name.all()} 
#         incoming_ids = [] 
#         try: 
#             with transaction.atomic(): 
#                 for item_data in items_data: 
#                     item_id = item_data.pop('id', None) 
#                     if item_id and item_id in existing_items: 
#                         item_instance = existing_items[item_id] 
#                         for attr, value in item_data.items(): 
#                             setattr(item_instance, attr, value) 
#                         item_instance.save() 
#                         incoming_ids.append(item_id) 
#                     else: 
#                         YourDetailsModel.objects.create(parent=instance, **item_data) 

#             # Delete removed items 
#             for existing_id in existing_items: 
#                 if existing_id not in incoming_ids: 
#                     existing_items[existing_id].delete() 
#         except Exception as e: 
#             return response_error(str(e), status=500, message='Internal server error) 
#         return instance 

