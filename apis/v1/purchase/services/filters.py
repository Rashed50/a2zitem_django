from django.db.models import Q, Prefetch, F, Count, Value 

##? Utils Import 

#from apis.utils.time import StartDate, EndDate 

##? Models Import 

#from apps.{app_name}.models import YourModel 

#class YourFilterService: 
#    def __init__(self, 
#        supplier_id = None, 
#        start_date = None, 
#        end_date = None, 
#    ): 
#        self.supplier_id = supplier_id 
#        self.start_date = start_date 
#        self.end_date = end_date 

#    def apply_filters(self, queryset): 
#        if self.supplier_id: 
#            queryset = queryset.filter(supplier_id=self.supplier_id) 
#        if self.start_date: 
#            queryset =  queryset.filter(date__gte=DateStart(self.start_date)) 
#        if self.end_date: 
#            queryset =  queryset.filter(date__lte=DateEnd(self.end_date)) 
#        return queryset 
