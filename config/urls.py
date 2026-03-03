from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

##? For Language Translation
from core.views.language_test import TranslationTestView

from theme import views

urlpatterns = [
    ##? Client URL
    path('', include('clientpage.urls')),
    
    ##? Admin URL
    path('admin1/', admin.site.urls),
    
    ##? Django Admin URL
    path('admin/', include('apps.urls')),
    
    ##? APIs
    path('api/', include('apis.urls')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    ##? Dark Mood Test
    # path('', views.home, name='home'), ## Dark Mood test
    path('toggle/', views.toggle_theme, name='toggle_theme'),
    
    ##? For Language Translation
    path('i18n/', include('django.conf.urls.i18n')),
    path('translation-test/', TranslationTestView.as_view(), name='translation_test'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
##! Django Browser Reload (Tailwind CSS)    
if not settings.LIVE:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]