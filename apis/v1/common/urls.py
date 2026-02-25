from django.urls import path, include

app_name = 'common_api'

##? Common APIs
from apis.v1.common.rich_text_media import views as rich_text_media_views
from apis.v1.common.role import views as role_views
from apis.v1.common.permission import views as permission_views
from apis.v1.common.user import views as user_views
from apis.v1.common.religion.views import ReligionApiView as religion_view


urlpatterns = [
    ##? Role/Group
    path(
        'role/',
        include(
            [
                ## POST (create) & GET (list)
                path('', role_views.GroupListCreateAPIView.as_view()), 
                ## GET (retrieve), PUT/PATCH (update), # DELETE (delete) 
                path('<int:id>/', role_views.GroupRetrieveUpdateDestroyAPIView.as_view()), 
            ]
        ),
   ),
   
    ##? Permission
    path(
        'permission/',
        include(
            [
                path('', permission_views.PermissionListAPIView.as_view()),  # GET (list)
            ]
        ),
    ),
   
    ##? User
    path('user-choices/', user_views.UserChoicesAPIView.as_view()),  # GET (list)
    path(
        'my/',
        include(
            [
                path('roles-permissions/', user_views.UserRolesAndPermissionsAPIView.as_view()),  # GET (list)
            ]
        ),
    ),
   
    ##? Rich Text Editor Media
    path(
        'rich-text-editor-media/',
        include(
            [
                ## POST (create)
                path('', rich_text_media_views.RichTextEditorMediaListCreateAPIView.as_view()),  
                ## GET (retrieve), PUT/PATCH (update), # DELETE (delete)
                path('<int:id>/', rich_text_media_views.RichTextEditorMediaUpdateDestroyAPIView.as_view()), 
            ]
        ),
    ),

    ##? Religion
    path(
        'religion/',
        include(
            [
                path('', religion_view.ReligionListAPIView.as_view()),  # GET (list)
            ]
        ),
    ),
]
