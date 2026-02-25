from django.contrib.auth.models import Group


def user_groups_processor(request):
    if request.user.is_authenticated:
        # print("-------------------------")
        # print(request.user)
        # print("User Group =", request.user.groups.values_list('name', flat=True))
        # print("-------------------------")
        
        #? Groups
        user_groups_qs = request.user.groups.values_list('name', flat=True)
        
        #? Permissions
        permissions_qs = request.user.get_all_permissions()
        
        # return {'user_groups': request.user.groups.values_list('name', flat=True)}
        return {
            'user_groups': user_groups_qs,                  # QuerySet
            'user_groups_list': list(user_groups_qs),       # List
            
            'user_permissions': permissions_qs,             # QuerySet
            'user_permissions_list': list(permissions_qs),  # List
            
            'is_superuser': request.user.is_superuser,
            'is_staff': request.user.is_staff,
        }
        
    # return {'user_groups': []}
    return {
        'user_groups': [],
        'user_groups_list': [],
    }