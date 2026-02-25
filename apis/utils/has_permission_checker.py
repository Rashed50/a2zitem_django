from apis.utils.permission_checker import check_user_permission
from apis.utils.group_checker import user_in_group

def has_access(user, required_perms=None, required_groups=None, require_all=False):
    """
    Check if a user has either the required permissions OR belongs to the required groups.
    Returns True if user satisfies ANY of the conditions.
    """
    if not user or not user.is_authenticated:
        return False

    # Check permissions
    if required_perms:
        if check_user_permission(user, required_perms, require_all=require_all):
            return True

    # Check groups
    if required_groups:
        if user_in_group(user, required_groups):
            return True

    return False


"""
## NOTE Example:-

def create(self, request, *args, **kwargs):
    ##* Permission & group check
    if not has_access(
        request.user,
        required_perms=["events.add_event"],
        required_groups=["Admin", "Moderator"]
    ):
        return response_permission_denied(["events.add_event"])
    
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return response_create(serializer.data,item_name="Event")
"""