from rest_framework.pagination import PageNumberPagination

class CasePagination(PageNumberPagination):
    page_size = 5
    page_query_param = "pagenum" 
    invalid_page_message = "Invalid page number"
    page_size_query_param = "size"
    max_page_size = 10