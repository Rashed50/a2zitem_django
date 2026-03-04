from django.urls import path, include 

app_name = 'product' 

##? Import Views 
from apps.product.views.brandView import BrandListPageView
from apps.product.views.colorView import ColorListPageView
from apps.product.views.sizeView import SizeListPageView
from apps.product.views.unitView import UnitListPageView
from apps.product.views.cagegoryView import CategoryListPageView


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
        ])
    )
    # path(
    #     'subscription/',
    #     include(
    #         [
    #             path('list/', views.SubscriptionTemplatePage.as_view(), name='subscription_list_page'),
    #             path('create/', views.SubscriptionCreatePage.as_view(), name='subscription_create_page'),
    #             path('details/<int:pk>/', views.SubscriptionDetailsPage.as_view(), name='subscription_details_page'),
    #             path('update/<int:pk>/', views.SubscriptionUpdatePage.as_view(), name='subscription_update_page'),
    #         ]
    #     )
    # )
]