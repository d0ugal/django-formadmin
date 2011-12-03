from django.contrib import admin

from formadmin.admin import FormAdmin


class AlreadyRegistered(Exception):
    pass


def register(form, admin_class=None, admin_site=None):

    if not admin_class:
        admin_class = FormAdmin

    if not admin_site:
        admin_site = admin.site

    # Instantiate the admin class to save in the registry
    admin_class_instance = admin_class(form, admin_site)

    for model_like_form, form_admin in admin_site._registry.items():
        if form_admin.form == form:
            raise AlreadyRegistered('The form %s is already registered' % form.__name__)

    admin_site._registry[admin_class_instance.model] = admin_class_instance
