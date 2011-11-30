from django.contrib.admin import ModelAdmin
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from formadmin.hacks import fake_model, fake_queryset

csrf_protect_m = method_decorator(csrf_protect)


class FormAdmin(ModelAdmin):

    model = True

    def __init__(self, form, admin_site):

        self.model = fake_model()
        form._meta = self.model._meta
        self.opts = self.model._meta
        self.admin_site = admin_site

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return True

    def has_delete_permission(self, *args, **kwargs):
        return True

    def queryset(self, request):

        return self.get_column_data(request)

    def column_display(self):
        pass

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        from formadmin.views import ChangeList
        return ChangeList

    def get_admin_choices(self, *args, **kwargs):
        return []

    def get_action_choices(self, *args, **kwargs):
        return []

    def get_column_data(self, request):

        return fake_queryset(self.column_data(request))

    @property
    def __name__(self,):
        return "FormAdminName"
