from rest_framework import serializers

##? Models Import
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    module    = serializers.CharField(source="content_type.model", read_only=True)
    app_label = serializers.CharField(source="content_type.app_label", read_only=True)

    class Meta:
        model  = Permission
        fields = [
            "id",
            "name",
            "codename",
            "module",
            "app_label",
        ]
        
