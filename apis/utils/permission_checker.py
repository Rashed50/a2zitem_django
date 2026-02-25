from django.contrib.auth.models import Permission

def check_user_permission(user, perms, debug=False, require_all=False) -> bool:
    """
    Check whether a user has one or multiple permissions.
    Works for:
      ✅ Superusers
      ✅ Direct user permissions
      ✅ Group-based permissions

    Args:
        user: Django User instance
        
        perms (str | list): single permission or list of permissions
        
        Example: "company.add_subscriptionplan" or ["company.add_subscriptionplan", "company.change_subscriptionplan"]
            
        debug (bool): If True, prints debug info
        
        require_all (bool): If True, user must have ALL permissions.
                            If False (default), having ANY one permission is enough.

    Returns:
        bool: True if condition is satisfied, False otherwise.

    """

    if not user or not user.is_authenticated:
        if debug: print("❌ User not authenticated")
        return False

    if getattr(user, "is_superuser", False):
        if debug: print("✅ Superuser: all permissions granted")
        return True

    # Convert single string to list
    if isinstance(perms, str):
        perms = [perms]

    results = [user.has_perm(p) for p in perms]

    if debug:
        print("🔍 Checking permissions:", perms)
        print("➡️ Results:", results)
        print("👤 Groups:", list(user.groups.values_list('name', flat=True)))
        print("👤 Direct permissions:", list(user.user_permissions.values_list('codename', flat=True)))

    # Require all or any
    return all(results) if require_all else any(results)




"""
##! Usage Examples:-
##? 1️⃣ Check single permission:
check_user_permission(request.user, "company.add_subscriptionplan")


##? 2️⃣ Check multiple (ANY one is enough ✅):
check_user_permission(request.user, [
    "company.add_subscriptionplan",
    "company.change_subscriptionplan"
])

##? 3️⃣ Check multiple (MUST have all ✅):
check_user_permission(request.user, [
    "company.add_subscriptionplan",
    "company.delete_subscriptionplan"
], require_all=True)

##? 4️⃣ With debug info:
check_user_permission(request.user, ["company.add_subscriptionplan"], debug=True)
"""