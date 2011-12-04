Django FormAdmin
========================================

FormAdmin is a simple app that allows you to add Form's to Django's admin that
are not related in any way to Models. The provided FormAdmin class is to Form
subclasses as Django's ModelAdmin is to Model subclasses.

To install FormAdmin::

    pip install django-formadmin

The simplest usage, add these lines to your admin.py::

    from formadmin import sites
    from myproject.forms import EmailForm

    sites.register(EmailForm)

This approach registers `MyForm` to the default admin site, with no further
customisations.

If you want to change the presentation, there are a few settings that you can
tweak. The following example shows how you can change the name in the admin
index, and the app label that it appears under::

    from formadmin.admin import FormAdmin

    class EmailFormAdmin(FormAdmin):
        app_label = "AdminForms"
        verbose_name = "Email Staff"

    sites.register(EmailForm, EmailFormAdmin)

The app_label doesn't need to be unique, you can use this as a neat trick to add
forms in the admin under existing apps such as contrib.auth