from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.contrib.auth import get_user_model

##? Utils Import
from apis.utils.apiResponse import *

##? Models Import
User = get_user_model()
from django.contrib.auth.models import Permission

##? Serializers Import
from apis.v1.common.user.serializers import UserRolePermissionSerializer, UserChoicesSerializer


class UserRolesAndPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserRolePermissionSerializer(user)
        return response_details(serializer.data, item_name="User Role/Group and Permissions")
    
class UserChoicesAPIView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        serializer = UserChoicesSerializer({})
        return response_details(serializer.data, item_name="User all choices data")

