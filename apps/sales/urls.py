from django.urls import path, include 

app_name = 'sales' 

##? Import Views 
from apps.sales.views import (
    SaleListPageView,
    SaleCreatePageView,
    SaleDetailPageView,
    SaleUpdatePageView
)

urlpatterns = [ 
    path('', SaleListPageView.as_view(), name='sale_list_page'),
    path('create/', SaleCreatePageView.as_view(), name='sale_create_page'),
    path('details/<int:pk>/', SaleDetailPageView.as_view(), name='sale_details_page'),
    path('update/<int:pk>/', SaleUpdatePageView.as_view(), name='sale_update_page'),
]