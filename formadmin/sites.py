from django.contrib import admin

from formadmin.admin import FormAdmin


class AlreadyRegistered(Exception):
    pass


def register(form, admin_class=None, admin_site=None, **options):

    if not admin_class:
        admin_class = FormAdmin

    if not admin_site:
        admin_site = admin.site

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
    admin_site._registry[form] = admin_class(form, admin.site)
