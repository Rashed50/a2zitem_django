from django.urls import path, include 

app_name = 'supplier_api' 

##? APIs Import 
from apis.v1.supplier.views.supplier import (
    SupplierListCreateAPIView, 
    SupplierRetrieveUpdateDestroyAPIView
)

urlpatterns = [ 
    ## GET (List) & POST (Create)
    path('', SupplierListCreateAPIView.as_view()), 
    ## GET (Details), PUT/PATCH (Update), DELETE (Delete)    
    path('<int:pk>/', SupplierRetrieveUpdateDestroyAPIView.as_view()),         
] 


