from django.db.models import Q, Prefetch, F, Count, Value 

##? Utils Import 
from apis.utils.time import StartDate, EndDate 

##? Models Import 
from apps.product.models.category import Category
from apps.product.models.brand import Brand
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure



class BrandFilterService:
    def __init__(
        self,
        search      = None,
        is_active   = None,
        start_date  = None,
        end_date    = None,
        ordering    = None,
    ):
        self.search      = search
        self.is_active   = is_active
        self.start_date  = start_date
        self.end_date    = end_date
        self.ordering    = ordering
        
    def apply_filters(self, queryset):
        ##* 🔍 Search filter 
        if self.search:
            queryset = queryset.filter(
                Q(name__icontains=self.search) 
                | Q(slug__icontains=self.search)
                | Q(id__exact=self.search)
            )
        ##* 🔎 Filter
        if self.is_active is not None:
            is_active = self.is_active
            if isinstance(is_active, str):
                is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)
        if self.start_date:
            queryset = queryset.filter(created_at__gte=StartDate(self.start_date))
        if self.end_date:
            queryset = queryset.filter(created_at__lte=EndDate(self.end_date))
            
        ##* ↕ Ordering
        if self.ordering:
            queryset = queryset.order_by(self.ordering)
        return queryset


class ColorFilterService:
    def __init__(
        self,
        search      = None,
        is_active   = None,
        start_date  = None,
        end_date    = None,
        ordering    = None,
    ):
        self.search      = search
        self.is_active   = is_active
        self.start_date  = start_date
        self.end_date    = end_date
        self.ordering    = ordering
        
    def apply_filters(self, queryset):
        ##* 🔍 Search filter 
        if self.search:
            queryset = queryset.filter(
                Q(name__icontains=self.search) 
                | Q(id__exact=self.search)
            )
        ##* 🔎 Filter
        if self.is_active is not None:
            is_active = self.is_active
            if isinstance(is_active, str):
                is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)
        if self.start_date:
            queryset = queryset.filter(created_at__gte=StartDate(self.start_date))
        if self.end_date:
            queryset = queryset.filter(created_at__lte=EndDate(self.end_date))
            
        ##* ↕ Ordering
        if self.ordering:
            queryset = queryset.order_by(self.ordering)
        return queryset


class SizeFilterService:
    def __init__(
        self,
        search      = None,
        is_active   = None,
        start_date  = None,
        end_date    = None,
        ordering    = None,
    ):
        self.search      = search
        self.is_active   = is_active
        self.start_date  = start_date
        self.end_date    = end_date
        self.ordering    = ordering
    
    def apply_filters(self, queryset):
    ##* 🔍 Search filter 
        if self.search:
            queryset = queryset.filter(
                Q(name__icontains=self.search) 
                | Q(id__exact=self.search)
            )
        ##* 🔎 Filter
        if self.is_active is not None:
            is_active = self.is_active
            if isinstance(is_active, str):
                is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)
        if self.start_date:
            queryset = queryset.filter(created_at__gte=StartDate(self.start_date))
        if self.end_date:
            queryset = queryset.filter(created_at__lte=EndDate(self.end_date))
            
        ##* ↕ Ordering
        if self.ordering:
            queryset = queryset.order_by(self.ordering)
        return queryset
        

class UnitOfMeasureFilterService:
    def __init__(
        self,
        search      = None,
        is_active   = None,
        start_date  = None,
        end_date    = None,
        ordering    = None,
    ):
        self.search      = search
        self.is_active   = is_active
        self.start_date  = start_date
        self.end_date    = end_date
        self.ordering    = ordering
        
    def apply_filters(self, queryset):
        ##* 🔍 Search filter 
        if self.search:
            queryset = queryset.filter(
                Q(name__icontains=self.search) 
                | Q(symbol__icontains=self.search)
                | Q(id__exact=self.search)
            )
        ##* 🔎 Filter
        if self.is_active is not None:
            is_active = self.is_active
            if isinstance(is_active, str):
                is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)
        if self.start_date:
            queryset = queryset.filter(created_at__gte=StartDate(self.start_date))
        if self.end_date:
            queryset = queryset.filter(created_at__lte=EndDate(self.end_date))
            
        ##* ↕ Ordering
        if self.ordering:
            queryset = queryset.order_by(self.ordering)
        return queryset
        
    

class CategoryFilterService:
    def __init__(
        self,
        search      = None,
        is_active   = None,
        parent_id   = None,
        category_id = None,
        start_date  = None,
        end_date    = None,
        ordering    = None,
    ):
        self.search      = search
        self.is_active   = is_active
        self.parent_id   = parent_id
        self.category_id = category_id
        self.start_date  = start_date
        self.end_date    = end_date
        self.ordering    = ordering

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
        
        if self.category_id:
            # category = Category.objects.get(id=self.category_id)
            # queryset = queryset.filter(tree_id=category.tree_id, lft__gte=category.lft, rght__lte=category.rght)
            print('=================')
            print(self.category_id)
            print('=================')
            if self.parent_id == "null":
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(parent_id=self.category_id)

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



