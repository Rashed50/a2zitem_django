"""
##! HR Permission Set
"""
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def get_hr_permissions():
    permissions = []
    
    ##? User ================================================
    User     = apps.get_model("users", "User")
    user_ct = ContentType.objects.get_for_model(User)

    permissions += Permission.objects.filter(
        content_type = user_ct,
        codename__in = [
            "add_user",
            "view_user",
            "change_user",
        ]

    )
    return permissions
