from django.db.models import Q, F, Count, Value, Prefetch 

##? Models Import 
from apps.supplier.models import Supplier

class SupplierQueryService:

    @staticmethod
    def get_queryset(search=None):
        queryset = Supplier.objects.select_related(
            'created_by',
            'updated_by',
        ).annotate(
            created_by_name = F('created_by__email'),
            updated_by_name = F('updated_by__email'),
        ).filter(
            # is_active  = True,
            is_deleted = False
        )

        # 🔎 Search Filter
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) 
                | Q(contact__icontains=search) 
                | Q(email__icontains=search) 
                | Q(phone__icontains=search)
            )

        return queryset.order_by('name').distinct()



#from apps.{app_name}.models import YourModel, RelatedModel 

# def YourQueryService: 
#     queryset = InboundCourier.objects.select_related( 
#         'related_field1', 
#         'related_field2', 
#         'related_field3', 
#         'related_field4', 
#     ).prefetch_related( 
#         Prefetch('related_set1', queryset=RelatedModel1.objects.all()), 
#         Prefetch('related_set2', queryset=RelatedModel2.objects.all()), 
#         Prefetch('related_set3', queryset=RelatedModel3.objects.all()), 
#         Prefetch('related_set4', queryset=RelatedModel4.objects.all()), 
#     ).annotate( 
#         field1_count=Count('related_field1'), 
#         field2_count=Count('related_field2'), 
#         field3_count=Count('related_field3'), 
#         field4_count=Count('related_field4'), 
#     ).filter( 
#         Q(field1=F('related_field1')) 
#         | Q(field2=F('related_field2')) 
#         | Q(field3=F('related_field3')) 
#         | Q(field4=F('related_field4')) 
#     ).order_by('-created_at').distinct() 
#     return queryset 
