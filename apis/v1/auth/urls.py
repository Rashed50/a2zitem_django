from django.urls import path 

from apis.v1.auth.views import registrations, login

urlpatterns = [ 
    path('registration/', registrations.UserRegistrationAPIView.as_view()), 
    path('login/', login.LoginAPIView.as_view()),


    # path('', AuthView.as_view(), name='list'), 
    # path('<int:pk>/', AuthView.as_view(), name='details'), 
] 
