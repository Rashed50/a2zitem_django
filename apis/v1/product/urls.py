from django.urls import path, include 

app_name = 'product_api' 

##? APIs Import 
from apis.v1.product.views.productApiView import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView

urlpatterns = [ 
    ## POST (Create)
    path('', ProductListCreateAPIView.as_view()), 
    ## GET (Details), PUT/PATCH (Update), DELETE (Delete)
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()), 
] 


