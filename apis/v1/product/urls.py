from django.urls import path, include 

#app_name = 'Your APP Name' 

##? APIs Import 

urlpatterns = [ 
#    path('', YourCreateAPIView.as_view(), name='your_app_name.create'), # POST (Create)
#    path('', YourListAPIView.as_view(), name='your_app_name.list'), # GET (List) 
#    path('<int:id>/', YourDetailAPIView.as_view(), name='your_app_name.details'), # GET (Details) 
#    path('<int:id>/update/', YourUpdateAPIView.as_view(), name='your_app_name.update'), # PUT/PATCH (Update) 
#    path('<int:id>/delete/', YourDeleteAPIView.as_view(), name='your_app_name.delete'), # DELETE (Delete) 
#    ##? Combined APIs 
#    path('', YourListCreateAPIView.as_view(), name='your_app_name.list_create'), # GET (List) & POST (Create) 
#    path('<int:id>/', YourRetrieveUpdateDestroyAPIView.as_view(), name='your_app_name.retrieve_update_destroy'), # GET (Details), PUT/PATCH (Update), DELETE (Delete) 


#    path( 
#        'your_path' 
#        include([ 
#            path('create/', YourCreateAPIView.as_view(), name='your_app_name.create'), 
#            path('list/', YourListAPIView.as_view(), name='your_app_name.list'), 
#            path('<int:id>/', YourDetailAPIView.as_view(), name='your_app_name.details'), 
#            path('<int:id>/update/', YourUpdateAPIView.as_view(), name='your_app_name.update'), 
#            path('<int:id>/delete/', YourDeleteAPIView.as_view(), name='your_app_name.delete'), 
#        ]) 
#    ), 
] 


