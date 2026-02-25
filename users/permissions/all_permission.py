"""
##! All Permission 
"""

from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

PERMISSION_MAP = {
    "company.Department": {
        "add"    : "add_department",
        "view"   : "view_department",
        "change" : "change_department",
        "delete" : "delete_department",
    },
    "company.Designation": {
        "add"    : "add_designation",
        "view"   : "view_designation",
        "change" : "change_designation",
        "delete" : "delete_designation",
    },
    "employee.Employee": {
        "add"    : "add_employee",
        "view"   : "view_employee",
        "change" : "change_employee",
        "delete" : "delete_employee",
        # "approve_leave": "approve_leave_employee",
    },
}

def get_permissions_for_model(model_path: str, actions: list[str]) -> list:
    if model_path not in PERMISSION_MAP:
        return []

    codenames = []
    model_map = PERMISSION_MAP[model_path]

    for action in actions:
        if action in model_map:
            codenames.append(model_map[action])
        else:
            print(f"Warning: Action '{action}' not found for {model_path}")

    if not codenames:
        return []

    try:
        app_label, model_name = model_path.split(".")
        Model = apps.get_model(app_label, model_name)
        ct    = ContentType.objects.get_for_model(Model)
        
        return list(Permission.objects.filter(
            content_type = ct,
            codename__in = codenames
        ))
    except Exception as e:
        print(f"Error loading permissions for {model_path}: {e}")
        return []