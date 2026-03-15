from django.urls import path, include 

app_name = 'attributes_api' 

# {{BaseUrl}}/product-attributes/

##? APIs Import 
from apis.v1.attributes.views.brandApiView import (
        BrandListCreateAPIView, 
        BrandRetrieveUpdateDestroyAPIView,
        MiniBrandListApiView,
    )
from apis.v1.attributes.views.colorApiView import (
        ColorListCreateAPIView, 
        ColorRetrieveUpdateDestroyAPIView,
        MiniColorListApiView,
    )
from apis.v1.attributes.views.sizeApiView import (
        SizeListCreateAPIView, 
        SizeRetrieveUpdateDestroyAPIView,
        MiniSizeListApiView,
    )
from apis.v1.attributes.views.unitApiView import (
        UnitOfMeasureListCreateAPIView, 
        UnitOfMeasureRetrieveUpdateDestroyAPIView,
        MiniUnitOfMeasurListApiView,
    )
from apis.v1.attributes.views.categoryApiView import (
        CategoryListCreateAPIView, 
        CategoryRetrieveUpdateDestroyAPIView,  
        MiniCategoryListAPIView,
    )

urlpatterns = [ 
    path( 
        'brand/', 
        include([ 
            path('', BrandListCreateAPIView.as_view()),  
            path('<int:pk>/', BrandRetrieveUpdateDestroyAPIView.as_view()), 
            path('mini-list/', MiniBrandListApiView.as_view()),
        ]) 
    ), 
    path( 
        'color/', 
        include([ 
            path('', ColorListCreateAPIView.as_view()),  
            path('<int:pk>/', ColorRetrieveUpdateDestroyAPIView.as_view()), 
            path('mini-list/', MiniColorListApiView.as_view()),
        ]) 
    ), 
    path( 
        'size/', 
        include([ 
            path('', SizeListCreateAPIView.as_view()),  
            path('<int:pk>/', SizeRetrieveUpdateDestroyAPIView.as_view()), 
            path('mini-list/', MiniSizeListApiView.as_view()),
        ]) 
    ),
    path( 
        'unit/', 
        include([ 
            path('', UnitOfMeasureListCreateAPIView.as_view()),  
            path('<int:pk>/', UnitOfMeasureRetrieveUpdateDestroyAPIView.as_view()), 
            path('mini-list/', MiniUnitOfMeasurListApiView.as_view()),
        ]) 
    ),
    path( 
        'category/', 
        include([ 
            path('', CategoryListCreateAPIView.as_view()),  
            path('<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view()), 
            path('mini-list/', MiniCategoryListAPIView.as_view()),
        ]) 
    ),
] 


