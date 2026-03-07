from django.urls import path, include 

app_name = 'product' 

##? Import Views 
from apps.product.views.brandView import BrandListPageView
from apps.product.views.colorView import ColorListPageView
from apps.product.views.sizeView import SizeListPageView
from apps.product.views.unitView import UnitListPageView
from apps.product.views.cagegoryView import (
    CategoryListPageView, 
    CategoryCreatePageView,
    CategoryUpdatePageView,
    CategoryDetailsPageView
)

from apps.product.views.productView import (
    ItemListPageView,
    ProductListPageView,
)

urlpatterns = [ 
    path('brand/', BrandListPageView.as_view(), name='brand_list_page'),
    path('color/', ColorListPageView.as_view(), name='color_list_page'),
    path('size/', SizeListPageView.as_view(), name='size_list_page'),
    path('unit-of-measurment/', UnitListPageView.as_view(), name='unit_list_page'),
    
    ##? Category 
    path(
        'category/', 
        include([
            path('', CategoryListPageView.as_view(), name='category_list_page'),
            path('create/', CategoryCreatePageView.as_view(), name='category_create_page'),
            path('update/<int:pk>/', CategoryUpdatePageView.as_view(), name='category_update_page'),
            path('details/<int:pk>/', CategoryDetailsPageView.as_view(), name='category_details_page'),
        ])
    ),
    
    ##? Product
    path(
        '', 
        include([
            path('', ProductListPageView.as_view(), name='product_list_page'),
        ])
    ),
    ##? Product Item
    path(
        'item/', 
        include([
            path('', ItemListPageView.as_view(), name='product_item_list_page'),
        ])
    ),
]