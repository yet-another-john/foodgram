"""Pagination class."""

from rest_framework.pagination import PageNumberPagination


class LimitPaginator(PageNumberPagination):
    """Jграничение вывода."""

    page_size_query_param = 'limit'
