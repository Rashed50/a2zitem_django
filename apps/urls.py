from django.urls import path, include

urlpatterns = [
    path('', include('apps.auth.urls',  namespace='auth')),
    path('', include('apps.dashboard.urls',  namespace='dashboard')),
    path('components/', include('apps.components.urls',  namespace='components')),
    path('roles/', include('apps.roles.urls',  namespace='roles')),
    path('product/', include('apps.product.urls',  namespace='product')),
    path('sales/', include('apps.sales.urls',  namespace='sales')),
]