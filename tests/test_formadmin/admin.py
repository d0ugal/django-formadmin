from formadmin.admin import FormAdmin
from formadmin import sites

from test_formadmin.forms import EmailForm, UploadForm


class EmailFormAdmin(FormAdmin):
    verbose_name = "Email Form"
    verbose_name_plural = "Email Forms"


class UploadFormAdmin(FormAdmin):
    pass


sites.register(EmailForm, EmailFormAdmin)
sites.register(UploadForm, UploadFormAdmin)
