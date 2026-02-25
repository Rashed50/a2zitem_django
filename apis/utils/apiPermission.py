from rest_framework.permissions import BasePermission 
from apis.utils.group_checker import user_in_group 

from rest_framework import permissions 

##? Utils Import
from apis.utils.group_checker import user_in_group
from apis.utils.permission_checker import check_user_permission

##! Only Check Permission
class HasPermission(BasePermission):
    message = "You do not have permission to perform this action."
    # message = "Permission denied! Please contact the administrator."

    def has_permission(self, request, view):
        user = request.user
        
        # print('===========================')
        # print("Request User:", user)
        # print('===========================')
        
        ##? Authentication Check
        if not user or not user.is_authenticated:
            self.message = "Authentication required."
            return False

        ##? Superuser Always Allowed
        if user.is_superuser:
            return True
        
        ##? Permission Policy Check [Superuser, Admin]
        policy = getattr(view, "permission_policy", {}).get(request.method, {})
        if policy.get("superuser") and not request.user.is_superuser:
            return False
        if policy.get("admin") and not (request.user.is_admin or request.user.is_superuser):
            return False
        
        ##? Check Permissions
        required_perms = getattr(view, "required_perms", None)

        if not required_perms:
            return True

        if check_user_permission(user, required_perms):
            return True

        self.message = f"Missing permission(s): {required_perms}"
        return False


##! Check Permission + Group Both
class HasPermissionOrGroup(BasePermission):
    """
    Check if user has any of the required permissions OR belongs to any of the required groups.
    
    required_perms : list of permission codenames
    required_groups : list of group names
    require_all    : True => must have ALL permissions
    """
    required_perms  = []
    required_groups = []
    require_all     = False

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Superuser always allowed
        if getattr(user, "is_superuser", False):
            return True

        # Permissions check
        if self.required_perms:
            if check_user_permission(user, self.required_perms, require_all=self.require_all):
                return True

        # Group check
        if self.required_groups:
            if user_in_group(user, self.required_groups):
                return True

        return False

"""
## NOTE Example:-
from apis.utils.apiPermission import HasPermissionOrGroup

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer

    permission_classes = [
        HasPermissionOrGroup
    ]

    # Customize permissions per view
    def get_permissions(self):
        permission = HasPermissionOrGroup()
        permission.required_perms = ["events.add_event"]
        permission.required_groups = ["Admin", "Moderator"]
        return [permission]

"""


##! Only Superuser Allowed
class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to superusers.
    """
    message = "You do not have superuser privileges."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "is_superuser", False)
    
    
    
##! Only Admin/Staff Allowed  
class IsStaffUser(permissions.BasePermission):
    """
    Allows access to staff/admin users.
    """
    message = "You do not have staff/admin privileges."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, "is_admin", False)
     
     
     
     
     
##* ============================== [Takes from Groups] ==============================
##! Only Admin Allowed [Takes from Groups]
class IsAdminUser(permissions.BasePermission):
    """
    Allows access if user belongs to 'Admin' group OR has all permissions.
    """
    message = "Permission denied! Please contact the administrator."

    required_perms  = []      # Example: ["events.add_event"]
    required_groups = ["Admin"]

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Superuser always allowed
        if getattr(user, "is_superuser", False):
            return True

        # Check groups
        if user_in_group(user, self.required_groups):
            return True

        # Check permissions if any
        if self.required_perms and check_user_permission(user, self.required_perms):
            return True

        return False
   
   
   
##! Only Moderator Allowed [Takes from Groups]
class IsModeratorUser(permissions.BasePermission):
    """
    Allows access if user belongs to 'Moderator' group OR has any of the moderator permissions.
    """
    # message = "You do not have moderator privileges."
    message = "Permission denied! Please contact the administrator."

    required_perms  = []       # Example: ["events.add_event", "events.change_event"]
    required_groups = ["Moderator"]

    def has_permission(self, request, view):
        user = request.user
        
        # print("====================")
        # print("User:", user)
        # print("Groups:", user.groups.all())
        # print("Permissions:", user.user_permissions.all())
        # print("====================")
        
        if not user or not user.is_authenticated:
            return False

        ##? Superuser always allowed
        if getattr(user, "is_superuser", False):
            return True
        
        ##? Dynamic group check
        allowed_groups = getattr(self, "allowed_groups", [])
        if allowed_groups and user_in_group(user, allowed_groups):
            return True

        ##? Dynamic permission check
        required_perms = getattr(self, "required_perms", [])
        if required_perms and check_user_permission(user, required_perms):
            return True

        return False



##! Only User Allowed [Takes from Groups]
class IsUser(permissions.BasePermission):
    """
    Allows access if user belongs to 'User' group OR has any of the user permissions.
    """
    # message = "You do not have user privileges."
    message = "Permission denied! Please contact the administrator."

    required_perms  = []       # Example: ["events.view_event"]
    required_groups = ["User"]

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if getattr(user, "is_superuser", False):
            return True

        if user_in_group(user, self.required_groups):
            return True

        if self.required_perms and check_user_permission(user, self.required_perms):
            return True

        return False