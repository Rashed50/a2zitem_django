from django.urls import path, include 

app_name = 'roles' 

##? Import Views 
from apps.roles import views


urlpatterns = [ 
    path('', views.RolesListPageView.as_view(), name='roles_list_page'),
    path('create/', views.RoleCreatePageView.as_view(), name='role_create_page'),
    path('details/<int:pk>/', views.RoleDetailsPageView.as_view(), name='role_details_page'),
    path('update/<int:pk>/', views.RoleUpdatePageView.as_view(), name='role_update_page'),
    path('permissions/', views.PermmissionsListPageView.as_view(), name='permissions_list_page'),
] 