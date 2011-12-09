from django.db.models.options import Options

from formadmin import settings


def create_model_like_form(original_form, formadmin=None):
    """
    This is a horrific hack to make the admin accept a Form class. It takes a
    form instance, and optionally a form admin.

    It the dynamically creates a sublcass of the form, so we can monkeypatch it
    without changing the original. It then primarily adds a _meta property that
    adds a number of properties that the admin expects to be there for a model.
    """

    from formadmin.admin import FormAdmin

    if not formadmin:
        formadmin = FormAdmin

    name = "ModelLikeForm%s" % original_form.__name__
    form = type('AdminCompatible%s' % name, (original_form,), {})

    form.__name__ = original_form.__name__

    class Meta:
        pass

    meta = Options(Meta)
    meta.app_label = getattr(formadmin, 'app_label', settings.FORMADMIN_APP_LABEL)
    meta.module_name = original_form.__name__.lower()
    meta.verbose_name_plural = getattr(formadmin, 'verbose_name', original_form.__name__)
    meta.verbose_name = getattr(formadmin, 'verbose_name', original_form.__name__)
    meta.object_name = meta.module_name
    meta.managed = False

    form._meta = meta

    return form
