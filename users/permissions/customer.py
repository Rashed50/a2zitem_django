"""
##! User Permission Set
"""
from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def get_customer_permissions():
    permissions = []
    
    ##? Event ================================================
    # Event    = apps.get_model("events", "Event")
    # event_ct = ContentType.objects.get_for_model(Event)

    # permissions += Permission.objects.filter(
    #     content_type = event_ct,
    #     codename     = "view_event"
    # )

    ##? Announcement =========================================
    # Announcement    = apps.get_model("events", "Announcement")
    # announcement_ct = ContentType.objects.get_for_model(Announcement)

    # permissions += Permission.objects.filter(
    #     content_type = announcement_ct,
    #     codename     = "view_announcement"
    # )

    """
    ##! Note Work: 
    post_migrate সিগন্যাল users অ্যাপের মাইগ্রেশন শেষ হওয়ার পর চলছে — কিন্তু auth অ্যাপের সব
    মাইগ্রেশন এখনো শেষ হয়নি। তাই ContentType এন্ট্রি নেই।
    """
    ##? NEW: Django's default auth app থেকে Group এবং Permission এর view পারমিশন যোগ করো
    # Django auth.Group → view_group
    # permissions += Permission.objects.filter(
    #     content_type = ContentType.objects.get(app_label="auth", model="group"),
    #     codename     = "view_group"
    # )

    # # Django auth.Permission → view_permission
    # permissions += Permission.objects.filter(
    #     content_type = ContentType.objects.get(app_label="auth", model="permission"),
    #     codename     = "view_permission"
    # )
    
    return permissions
