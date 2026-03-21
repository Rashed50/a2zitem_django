from django.urls import path, include 

app_name = 'product_api' 

##? APIs Import 
from apis.v1.product.views.productApiView import (
    ProductListCreateAPIView, 
    ProductRetrieveUpdateDestroyAPIView,
    CusomerProductListAPIView,
    CustomerProductDetailsAPIView
)
from apis.v1.product.views.variantApiView import ProductVariantMiniListAPIView

urlpatterns = [ 
    ## POST (Create)
    path('', ProductListCreateAPIView.as_view()), 
    ## GET (Details), PUT/PATCH (Update), DELETE (Delete)
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view()), 
    
    ##? Variant
    path(
        'variant/',
        include([
            path('mini-list/', ProductVariantMiniListAPIView.as_view()),
        ]) 
    ),
    
    ##! For Customers 
    path(
        'customer/',
        include([
            path('product-list/', CusomerProductListAPIView.as_view()),
            path('product-details/<int:pk>/', CustomerProductDetailsAPIView.as_view()),
        ]) 
    ),
] 


