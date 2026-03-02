from rest_framework.permissions import BasePermission 
from apis.utils.group_checker import user_in_group 

#class IsInAllCommercialGroups(BasePermission): 
#     allowed_groups = ['INBOUND_COMMERCIAL', 'ADMIN'] 

#     def has_permission(self, request, view): 
#        return user_in_group(request.user, self.allowed_groups) or request.user.is_superuser 
