from django.apps import apps
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save, post_migrate

##? Permission Import
from users.permissions.admin import get_admin_permissions
from users.permissions.owner import get_owner_permissions
from users.permissions.moderator import get_moderator_permissions
from users.permissions.hr import get_hr_permissions
from users.permissions.customer import get_customer_permissions
from users.permissions.employee import get_employee_permissions

##? Model Import
User = get_user_model()


# @receiver(post_migrate)
# @receiver(post_migrate, dispatch_uid="create_default_groups_once")
@receiver(post_migrate, dispatch_uid="users_create_default_groups")
def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    """
    Create default user groups after migration
    
    SuperAdmin   (system owner, optional)
    Admin        (full access, business admin)
    HR           (employee management)
    Manager      (team-level control)
    Staff        (internal employee)
    Customer     (end user)
    Moderator    (content moderation)
    
    NOTE:- if sender.name != "users":
    👉 এর মানে: 
    - Django সব app এর migration শেষে এই signal fire করে
    - আমরা চাই শুধু users app migrate হলে run করুক
    - না হলে এক migration এ বারবার call হবে
    
    📌 Mute: if sender.name != "users":
    - post_migrate প্রতিটা app শেষে fire হয়
    - কিন্তু dispatch_uid থাকায় Django একবারই execute করবে
    - তখন সব permissions নিশ্চিতভাবে তৈরি হয়ে গেছে
    """
    ## Oly run for users app 
    # if sender.name != "users":
    #     return
    
    ##? Oly Groups Create
    # default_groups = [
    #     "Admin",
    #     "Moderator",
    #     "Event Manager",
    #     "User",
    # ]

    # for group_name in default_groups:
    #     Group.objects.get_or_create(name=group_name)
    
    ##? If Create Groups and Also Set Permissions
    # print("=====================================")
    # print("======== Moderator Permission Set ========")
    # print("Moderator =", get_moderator_permissions())
    # print("======== User Permission Set ========")
    # print("User =", get_user_permissions())
    # print("=====================================")
    
    groups_config = {
        "SuperAdmin" : Permission.objects.all(),     ## Full access
        "Admin"      : Permission.objects.all(),     ## Full access
        # "Admin"    : get_admin_permissions(),      ## Limited
        "Owner"      : get_owner_permissions(),      ## Limited 
        "Moderator"  : get_moderator_permissions(),  ## Limited 
        "Hr"         : get_hr_permissions(),         ## Limited
        "Employee"   : get_employee_permissions(),   ## Limited
        "Customer"   : get_customer_permissions(),   ## Limited
    }
    
    for group_name, permissions in groups_config.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        group.permissions.set(permissions)
        group.save()
    

    
        

