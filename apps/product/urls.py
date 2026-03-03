from django.urls import path, include 

app_name = 'product' 

##? Import Views 
from apps.product.views.brandView import BrandListPageView


urlpatterns = [ 
    path('brand/', BrandListPageView.as_view(), name='brand_list_page'),
    
    # ##? Subscription
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