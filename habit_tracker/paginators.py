from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Пагинация для просмотра привычек"""

    page_size = 5  # Количество элементов на странице
    page_size_query_param = "page_size"  # Параметр для указания размера страницы
    max_page_size = 100  # Максимально допустимый размер страницы
