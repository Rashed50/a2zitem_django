from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q

##? Models Import
User = get_user_model()
from django.contrib.auth.models import Group, Permission
from core.models.religion_model import Religion, ReligionDenomination
from core.constants import UserChoices, BangladeshConstants


class GroupMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Group
        fields = ["id", "name"]

class PermissionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Permission
        fields = ["id", "name", "codename"]

class UserRolePermissionSerializer(serializers.ModelSerializer):
    groups      = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ["id", "first_name", "last_name", "email", "groups", "permissions"]

    def get_groups(self, user):
        return GroupMiniSerializer(user.groups.all(), many=True).data

    def get_permissions(self, user):
        direct_perms = user.user_permissions.all()
        group_perms  = Permission.objects.filter(group__in=user.groups.all())
        all_perms    = (direct_perms | group_perms).distinct()
        return PermissionMiniSerializer(all_perms, many=True).data

class UserChoicesSerializer(serializers.Serializer):
    gender_choices        = serializers.SerializerMethodField()
    auth_provider_choices = serializers.SerializerMethodField()
    image_type_choices    = serializers.SerializerMethodField()
    address_type_choices  = serializers.SerializerMethodField()
    religions             = serializers.SerializerMethodField()
    company_types         = serializers.SerializerMethodField()
    subscription_plan_type     = serializers.SerializerMethodField()
    subscription_billing_cycle = serializers.SerializerMethodField()
    subscription_duration_type = serializers.SerializerMethodField()
    company_subscription_status = serializers.SerializerMethodField()
    company_subscription_action = serializers.SerializerMethodField()
    company_currency_choices    = serializers.SerializerMethodField()
    company_timezone_choices    = serializers.SerializerMethodField()
    company_language_choices    = serializers.SerializerMethodField()
    blood_group_choices   = serializers.SerializerMethodField()

    def get_gender_choices(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in User.GenderType.choices]

    def get_auth_provider_choices(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in User.AuthProvider.choices]

    def get_religions(self, obj):
        religions = Religion.objects.prefetch_related('denominations').all()
        return [
            {
                "value": religion.id,
                "label": religion.name,
                "denominations": [
                    {"value": d.id, "label": d.name}
                    for d in religion.denominations.all()
                ]
            }
            for religion in religions
        ]
    
    def get_company_currency_choices(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in BangladeshConstants.CurrencyChoices.choices]
    
    def get_company_timezone_choices(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in BangladeshConstants.TimezoneChoices.choices]
    
    def get_company_language_choices(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in BangladeshConstants.LanguageChoices.choices]
    
    def get_blood_group_choices(self, obj):
        return [{"value": choice[0], "label": choice[1]} for choice in UserChoices.BloodGroupChoices.choices]
    
