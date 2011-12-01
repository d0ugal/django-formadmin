from formadmin.admin import FormAdmin
from formadmin import sites

from test_formadmin.forms import EmailForm


class EmailFormAdmin(FormAdmin):
    pass

sites.register(EmailForm, EmailFormAdmin)
