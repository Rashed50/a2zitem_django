from django.db.models import Q, Prefetch 

#class YourSearchService: 
#    def __init__(self, search_value): 
#        self.search_value = search_value.strip() 

#    def apply_search(self, queryset): 
#        if self.search_value: 
#            queryset = queryset.filter( 
#                Q(field_name__icontains=self.search_value) 
#                | Q(another_field__icontains=self.search_value) 
#            ).distinct() 
#        return queryset 
