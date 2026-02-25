from django.contrib import admin 


##? Import Models 
from apps.components.models import * 

#@admin.register(YourModel) 
#class YourModelAdmin(admin.ModelAdmin): 
#    list_display  = ['id', 'name'] 
#    search_fields = ['id', 'name'] 
#    list_filter   = ['id', 'name'] 
#    ordering      = ['-created_at',] 
