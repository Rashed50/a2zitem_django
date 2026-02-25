from rest_framework import serializers
from core.models.file_model import RichTextEditorMediaFile
from django.contrib.contenttypes.models import ContentType

##? Utils Import
from apis.utils.field_error_messages import get_field_error_messages
from users.validators import DateOfBirthValidator, ImageValidator

class RichTextEditorMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = RichTextEditorMediaFile
        fields = [
            "id", "file", "content_type", "object_id", "file_type", "size", 
            "mime_type", "original_name", "checksum", "created_at", "updated_at"
        ]
        
        extra_kwargs = {
            "id"   : {"read_only": True},
            "file" : {
                "required"       : True, 
                "allow_null"     : False, 
                "error_messages" : get_field_error_messages('File', 'FileField')
            },
            "content_type" : {
                "required"       : False, 
                "allow_null"     : True, 
                "error_messages" : get_field_error_messages('Content Type', 'CharField')
            },
            "object_id" : {
                "required"       : False, 
                "allow_null"     : True, 
                "error_messages" : get_field_error_messages('Object ID', 'CharField')
            },
            "file_type"     : {"read_only": True},
            "size"          : {"read_only": True},
            "mime_type"     : {"read_only": True},
            "original_name" : {"read_only": True},
            "checksum"      : {"read_only": True},
            "created_at"    : {"read_only": True},
            "updated_at"    : {"read_only": True},
        }

