from django.urls import path, include

urlpatterns = [
    path('common/', include('apis.v1.common.urls'), name='common_api'),
    path('auth/', include('apis.v1.auth.urls'), name='auth_api'),
]