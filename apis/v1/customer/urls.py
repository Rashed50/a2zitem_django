from django.urls import path, include 

app_name = 'customer_api' 

##? APIs Import 
from apis.v1.customer.views import CustomerMiniListAPIView

urlpatterns = [ 
    path('mini-list/', CustomerMiniListAPIView.as_view()), 

] 