"""
##! Admin/Staff Permission Set
"""

from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def get_admin_permissions():
    permissions = []
    
    ##? User ===============================================
    User    = apps.get_model("users", "User")
    user_ct = ContentType.objects.get_for_model(User)

    permissions += Permission.objects.filter(
        content_type = user_ct,
        codename__in = [
            "add_user",
            "view_user",
            "change_user",
            "delete_user",
        ]
    )

    ##? Event ================================================
    # Event    = apps.get_model("events", "Event")
    # event_ct = ContentType.objects.get_for_model(Event)
    
    # permissions += Permission.objects.filter(
    #     content_type = event_ct,
    #     codename__in = [
    #         "add_event",
    #         "view_event",
    #         "change_event",
    #         "delete_event",
    #     ]
    # )

    ##? Announcement ========================================
    # Announcement    = apps.get_model("events", "Announcement")
    # announcement_ct = ContentType.objects.get_for_model(Announcement)

    # permissions += Permission.objects.filter(
    #     content_type = announcement_ct,
    #     codename__in = [
    #         "add_announcement",
    #         "view_announcement",
    #         "change_announcement",
    #         "delete_announcement",
    #     ]
    # )

    ##? EventParticipant =====================================
    # EventParticipant = apps.get_model("events", "EventParticipant")
    # participant_ct   = ContentType.objects.get_for_model(EventParticipant)

    # permissions += Permission.objects.filter(
    #     content_type = participant_ct,
    #     codename__in = [
    #         "view_eventparticipant",
    #         "change_eventparticipant",
    #         "delete_eventparticipant",
    #     ]
    # )

    return permissions
