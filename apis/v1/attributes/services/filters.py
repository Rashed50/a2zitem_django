from django.db.models import Q, Prefetch, F, Count, Value 

##? Utils Import 
from apis.utils.time import StartDate, EndDate 

##? Models Import 
from apps.product.models.category import Category



class CategoryFilterService:
    def __init__(
        self,
        search     = None,
        is_active  = None,
        parent_id  = None,
        start_date = None,
        end_date   = None,
        ordering   = None,
    ):
        self.search     = search
        self.is_active  = is_active
        self.parent_id  = parent_id
        self.start_date = start_date
        self.end_date   = end_date
        self.ordering   = ordering

    def apply_filters(self, queryset):

        ##* 🔍 Search filter 
        if self.search:
            queryset = queryset.filter(
                Q(name__icontains=self.search) |
                Q(slug__icontains=self.search)
            )

        ##* 🔎 Filter
        if self.is_active is not None:
            is_active = self.is_active
            if isinstance(is_active, str):
                is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)
            
        if self.parent_id is not None:
            if self.parent_id == "null":
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=self.parent_id)

        if self.start_date:
            queryset = queryset.filter(
                created_at__gte=StartDate(self.start_date)
            )

        if self.end_date:
            queryset = queryset.filter(
                created_at__lte=EndDate(self.end_date)
            )

        ##* ↕ Ordering
        if self.ordering:
            queryset = queryset.order_by(self.ordering)

        return queryset

# class YourFilterService: 
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
#            queryset =  queryset.filter(date__gte=StartDate(self.start_date)) 
#        if self.end_date: 
#            queryset =  queryset.filter(date__lte=EndDate(self.end_date)) 
#        return queryset 
