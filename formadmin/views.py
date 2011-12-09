from django.utils.http import urlencode
from django.contrib.admin.views.main import ChangeList as BaseChangelist

from formadmin.hacks import fake_queryset

# The system will display a "Show all" link on the change list only if the
# total result count is less than or equal to this setting.
MAX_SHOW_ALL_ALLOWED = 200

# Changelist settings
ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
TO_FIELD_VAR = 't'
IS_POPUP_VAR = 'pop'
ERROR_FLAG = 'e'

# Text to display within change-list table cells if the value is blank.
EMPTY_CHANGELIST_VALUE = '(None)'


class ChangeList(BaseChangelist):

    def __init__(self, *args, **kwargs):

        try:
            super(ChangeList, self).__init__(*args, **kwargs)
        except Exception as e:
            print e

    def get_filters(self, request):
        # Disable filters, not supported.
        return [], False

    def get_query_string(self, new_params=None, remove=None):
        if new_params is None:
            new_params = {}
        if remove is None:
            remove = []
        p = self.params.copy()
        for r in remove:
            for k in p.keys():
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                p[k] = v
        return '?%s' % urlencode(p)

    def get_results(self, request):

        results = self.model_admin.get_column_data(request)

        self.result_count = len(results)
        self.full_result_count = len(results)
        self.result_list = results
        self.can_show_all = True
        self.multi_page = False
        self.paginator = True

    def get_ordering(self, *args, **kwargs):
        return 'order_field', 'asc'

    def get_query_set(self, *args, **kwargs):

        return fake_queryset("hmm")

    def url_for_result(self, result):
        return '/'  # "%s/" % quote(getattr(result, self.pk_attname))
