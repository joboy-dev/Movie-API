# PageNumberPagination
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 10  # for page size
    page_query_param  = 'p' # customizign what will be shown as the query parameter. it is normally ?paage
    page_size_query_param = 'size'  # basically yo improve user experience if they want to show more stuff on the screen than the default one set by us
    max_page_size = 20  # maximum amount of stuff that can be displayed at once
    last_page_strings = 'end'  # value to pass into the page parameter to take the user to the last page. by default it is 'last'


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20
    limit_query_param  = 'limit'
    offfset_query_param  = 'start'


class WatchListCPagination(CursorPagination):
    page_size = 2
    ordering = 'created'  # normally it is -created thereby setting it to ascending order. Also we are specifying the field we want to order by, so the field must be in your model
    cursor_query_param = 'record'
