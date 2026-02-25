"""
##! Owner Permission Set
"""

from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

##? Utils Import
from users.permissions.all_permission import get_permissions_for_model


def get_owner_permissions():
    permissions = []
    
    permissions += get_permissions_for_model("company.Department",   ["add", "view", "change", "delete"])
    permissions += get_permissions_for_model("company.Designation",  ["add", "view", "change", "delete"])
    permissions += get_permissions_for_model("employee.Employee",    ["add", "view", "change", "delete"])

    return permissions
