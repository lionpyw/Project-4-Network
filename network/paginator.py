from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination




class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


def add_paginator(serialized_data, p_number):
    paginator = Paginator(serialized_data, 10)
    total_pages = paginator.num_pages
    pager = paginator.get_page(p_number)
    current = pager.number
    page_obj = pager.object_list
    previous = 0
    next_p = 0
    if pager.has_previous():
        previous = pager.previous_page_number()
    if pager.has_next():
        next_p = pager.next_page_number()
    context =           {"resources": page_obj,
                         "previous" : previous,
                         "next" : next_p,
                         "total" : total_pages,
                         "current" : current}
    return context