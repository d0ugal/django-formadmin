from formadmin.admin import FormAdmin
from formadmin import sites

from test_formadmin.forms import EmailForm, UploadForm


class EmailFormAdmin(FormAdmin):
    app_label = "AdminForms"
    verbose_name = "Email Staff"


class UploadFormAdmin(FormAdmin):
    verbose_name = "Upload Logo"

sites.register(EmailForm, EmailFormAdmin)
sites.register(UploadForm, UploadFormAdmin)
