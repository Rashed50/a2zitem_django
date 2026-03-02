from django.urls import path, include 

app_name = 'supplier' 

##? Import Views 
from apps.supplier import views


urlpatterns = [ 
    path('', views.SupplierListPageView.as_view(), name='supplier_list_page'),
    path('create/', views.SupplierCreatePageView.as_view(), name='supplier_create_page'),
    path('details/<int:pk>/', views.SupplierDetailsPageView.as_view(), name='supplier_details_page'),
    path('update/<int:pk>/', views.SupplierUpdatePageView.as_view(), name='supplier_update_page'),
] 
