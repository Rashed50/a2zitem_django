from urllib.parse import urlencode
from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10                        # Default page size
    page_size_query_param = 'page_size'   # Allow client to override
    max_page_size = 100                   # Maximum limit
    


"""
##? Parametier => page_size, page, search, ordering, pagination
"""
def get_paginated_response(queryset, request, serializer_class, pagination=1):

    search_query   = request.query_params.get('search')
    ordering_query = request.query_params.get('ordering')
    
    ##! Build filters dictionary
    filters = {
        'search'   : search_query,
        'ordering' : None,
        'filters'  : {}
    }
    
    # Process ordering if exists
    if ordering_query:
        direction = 'asc' if not ordering_query.startswith('-') else 'desc'
        field     = ordering_query.lstrip('-')
        filters['ordering'] = {field: direction}
    
    # Process other filters (excluding pagination and known params)
    known_params = ['page', 'page_size', 'search', 'ordering', 'pagination',]
    for param in request.query_params:
        if param not in known_params and request.query_params[param]:
            filters['filters'][param] = request.query_params[param]
    
    ##! Pagination Setup
    if pagination != 1:
        serializer = serializer_class(queryset, many=True)
        response_data = {
            'total_items': queryset.count(),
            'filters'    : filters,
            'results'    : serializer.data
        }
    else:
        try:
            page_size = int(request.query_params.get('page_size', 10))
        except ValueError:
            page_size = 10
            
        try:
            page_number = int(request.query_params.get('page', 1))
        except ValueError:
            page_number = 1
        
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = serializer_class(page_obj, many=True)
        
        base_url = request.build_absolute_uri(request.path_info)
        query_params = request.query_params.copy()
        
        def get_page_link(page_num):
            params = query_params.copy()
            params['page'] = page_num
            return f"{base_url}?{urlencode(params)}"
        
        total_pages = paginator.num_pages
        
        # Calculate showing_from and showing_to
        showing_from = (page_number - 1) * page_size + 1
        showing_to = showing_from + len(page_obj.object_list) - 1
        
        response_data = {
            'total_items': paginator.count,
            'filters'    : filters,
            'pagination' : {
                'page_size'   : page_size,
                'total_pages' : total_pages,
                'showing_from' : showing_from,
                'showing_to'   : showing_to,
                'current_page_number' : page_number,  
                'last_page_number'    : total_pages,
                'links': {
                    'first'    : get_page_link(1),
                    'last'     : get_page_link(total_pages),
                    'next'     : get_page_link(page_obj.next_page_number()) if page_obj.has_next() else None,
                    'previous' : get_page_link(page_obj.previous_page_number()) if page_obj.has_previous() else None,
                }
            },
            'results': serializer.data
        }
    
    return response_data
