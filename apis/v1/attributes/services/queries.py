from django.db.models import Q, F, Count, Value, Prefetch 

##? Models Import
from apps.product.models.brand import Brand
from apps.product.models.color import Color
from apps.product.models.size import Size
from apps.product.models.unit import UnitOfMeasure
from apps.product.models.category import Category


##TODO:- Query Services

##! Brand Query Service --------------------------------------------------------
class BrandQueryService:
    @staticmethod
    def get_queryset(search=None):
        queryset = Brand.objects.select_related(
            'created_by', 'updated_by'
            ).annotate(
                created_by_name = F('created_by__email'),
                updated_by_name = F('updated_by__email'),
            ).filter(is_deleted = False)

        # 🔎 Search Filter
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset.order_by('name').distinct()

##! Color Query Service --------------------------------------------------------
class ColorQueryService:
    @staticmethod
    def get_queryset(search=None):
        queryset = Color.objects.select_related(
            'created_by', 'updated_by'
            ).annotate(
                created_by_name = F('created_by__email'),
                updated_by_name = F('updated_by__email'),
            ).filter(is_deleted = False)

        # 🔎 Search Filter
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset.order_by('name').distinct()


##! Size Query Service --------------------------------------------------------
class SizeQueryService:
    @staticmethod
    def get_queryset(search=None):    
        queryset = Size.objects.select_related(
            'created_by', 'updated_by'
            ).annotate(
                created_by_name = F('created_by__email'),
                updated_by_name = F('updated_by__email'),
            ).filter(is_deleted = False)

        # 🔎 Search Filter
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset.order_by('name').distinct(
    )


##! Unit Query Service --------------------------------------------------------
class UnitOfMeasureQueryService:
    @staticmethod
    def get_queryset(search=None):
        queryset = UnitOfMeasure.objects.select_related(
            'created_by', 'updated_by'
            ).annotate(
                created_by_name = F('created_by__email'),
                updated_by_name = F('updated_by__email'),
            ).filter(is_deleted = False)

        # 🔎 Search Filter
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(full_name__icontains=search)
            )
        return queryset.order_by('name').distinct()
