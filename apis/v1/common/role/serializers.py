from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apis.v1.common.permission.constants import ALLOWED_PERMISSION_MODELS

class PermissionSerializer(serializers.ModelSerializer):
    app_label = serializers.CharField(source="content_type.app_label", read_only=True)
    module    = serializers.CharField(source="content_type.model", read_only=True)
    
    class Meta:
        model  = Permission
        fields = ["id", "name", "app_label", "module", "codename"]

class GroupMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Group
        fields = ["id", "name"]
        
class GroupListSerializer(serializers.ModelSerializer):
    total_permissions = serializers.IntegerField(source="permissions.count", read_only=True)
    class Meta:
        model  = Group
        fields = ["id", "name", "total_permissions"]

class GroupSerializer(serializers.ModelSerializer):
    ## 🔹 WRITE (POST / PUT / PATCH)
    permissions_ids = serializers.PrimaryKeyRelatedField(
        many       = True,
        queryset   = Permission.objects.all(),
        write_only = True,
        required   = False
    )
    
    ##🔹 READ (GET)
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "permissions",
            "permissions_ids",
        ]
        
    def _get_allowed_permission_ids(self):
        allowed_content_types = []

        for app_label, models in ALLOWED_PERMISSION_MODELS.items():
            allowed_content_types.extend(
                ContentType.objects.filter(
                    app_label=app_label,
                    model__in=models
                )
            )

        return set(
            Permission.objects.filter(
                content_type__in=allowed_content_types
            ).values_list("id", flat=True)
        )

    # 🔥 FILTER PERMISSIONS ON READ (LIST / RETRIEVE)
    def to_representation(self, instance):
        data = super().to_representation(instance)

        allowed_permission_ids = self._get_allowed_permission_ids()

        data["permissions"] = [
            perm for perm in data["permissions"]
            if perm["id"] in allowed_permission_ids
        ]

        return data
    
    # 🔐 Validate allowed permissions only
    def validate_permissions_ids(self, permissions):
        allowed_content_types = []

        for app_label, models in ALLOWED_PERMISSION_MODELS.items():
            allowed_content_types.extend(
                ContentType.objects.filter(
                    app_label = app_label,
                    model__in = models
                )
            )

        allowed_permission_ids = set(
            Permission.objects.filter(
                content_type__in=allowed_content_types
            ).values_list("id", flat=True)
        )

        for perm in permissions:
            if perm.id not in allowed_permission_ids:
                raise serializers.ValidationError(
                    f"Permission '{perm.codename}' is not allowed."
                )

        return permissions

    def create(self, validated_data):
        permissions = validated_data.pop("permissions_ids", [])
        group       = Group.objects.create(**validated_data)

        if permissions:
            group.permissions.set(permissions)

        return group

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions_ids", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if permissions is not None:
            instance.permissions.set(permissions)

        return instance

