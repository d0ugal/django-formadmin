from django.contrib import admin
from django.forms.forms import DeclarativeFieldsMetaclass as BaseForm

from formadmin import FormAdmin


class AlreadyRegistered(Exception):
    pass


def register(form_or_iterable, admin_class, **options):

    if not admin_class:
        admin_class = FormAdmin

    if isinstance(form_or_iterable, BaseForm):
        form_or_iterable = [form_or_iterable]

    for form in form_or_iterable:

        if form in admin.site._registry:
            raise AlreadyRegistered('The form %s is already registered' % form.__name__)

        # If we got **options then dynamically construct a subclass of
        # admin_class with those **options.
        if options:
            # For reasons I don't quite understand, without a __module__
            # the created class appears to "live" in the wrong place,
            # which causes issues later on.
            options['__module__'] = __name__
            admin_class = type("%sAdmin" % form.__name__, (admin_class,), options)

        # Instantiate the admin class to save in the registry
        admin.site._registry[form] = admin_class(form, admin.site)
