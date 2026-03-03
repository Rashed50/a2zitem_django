from django.urls import path, include

app_name = 'clientpage'

##? Views Import
from clientpage import views

urlpatterns = [
    path('', views.ClintPageView.as_view(), name='client_home_page'),
]