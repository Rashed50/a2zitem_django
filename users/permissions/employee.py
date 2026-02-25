"""
##! User Permission Set
"""
from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def get_employee_permissions():
    permissions = []
    
    return permissions