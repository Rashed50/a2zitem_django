from django.urls import path, include 

app_name = 'components' 

##? Import Views 
from apps.components import views 


urlpatterns = [ 
    path('form-template/', views.FormTemplateView.as_view(), name='form_template'),
    path('table-template/', views.TableTemplateView.as_view(), name='table_template'),
    path('button-template/', views.ButtonTemplateView.as_view(), name='button_template'),
    path('badges-template/', views.BadgesTemplateView.as_view(), name='badges_template'),
               
    #path('list/', ListPage.as_view(), name='product_list'), 
    #path('details/<int:id>/', DetailsPage.as_view(), name='product_details'), 
    #path( 
    #    'entry/', 
    #    include( 
    #        [ 
    #            path('create/', CreatePage.as_view(), name='product_create'), 
    #            path('list/', ListPage.as_view(), name='product_list'), 
    #            path('details/<int:id>/', DetailsPage.as_view(), name='product_details'), 
    #            path('update/<int:id>/', UpdatePage.as_view(), name='product_update'), 
    #            path('delete/<int:id>/', DeletePage.as_view(), name='product_delete'), 
    #        ] 
    #    ), 
    #), 
] 
