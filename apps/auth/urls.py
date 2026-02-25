from django.urls import path

##? View Import
from apps.auth.views import login
from apps.auth.views import logout

app_name = 'auth' 

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', logout.LogoutView.as_view(), name='logout'),
]