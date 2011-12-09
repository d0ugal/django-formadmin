from django import template
from django.contrib.admin import helpers
from django.contrib.admin import ModelAdmin
from django.db import models
from django.forms.formsets import all_valid
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.utils.encoding import force_unicode
from django.utils.functional import update_wrapper
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from formadmin.hacks import create_model_like_form

csrf_protect_m = method_decorator(csrf_protect)


class FormAdmin(ModelAdmin):

    def __init__(self, original_form, admin_site):

        form_model = create_model_like_form(original_form, self)

        self.form = original_form
        self.model = form_model

        self.admin_site = admin_site

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.add_view),
                name='%s_%s_add' % info,),

            # A changelist view name is expected, just give add path again.
            url(r'^$',
                wrap(self.add_view),
                name='%s_%s_changelist' % info,),
        )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        ordered_objects = opts.get_ordered_objects()
        context.update({
            'add': add,
            'change': change,
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request, obj),
            'has_delete_permission': self.has_delete_permission(request, obj),
            'has_file_field': True,
            'has_absolute_url': hasattr(self.model, 'get_absolute_url'),
            'ordered_objects': ordered_objects,
            'form_url': mark_safe(form_url),
            'opts': opts,
            'save_as': self.save_as,
            'save_on_top': self.save_on_top,
        })
        form_template = self.add_form_template
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(form_template or [
            "admin/%s/%s/change_form.html" % (app_label, opts.object_name.lower()),
            "admin/%s/change_form.html" % app_label,
            "admin/change_form.html"
        ], context, context_instance=context_instance)

    def get_form(self, request, obj=None, **kwargs):
        return self.form

    def save_form(self, request, form, change):
        return form

    def save_model(self, request, obj, form, change):
        pass

    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):

        model = self.model
        opts = model._meta

        Form = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = Form(request.POST, request.FILES)
            if form.is_valid():
                self.save_form(request, form, change=False)
                form_validated = True
            else:
                form_validated = False
                self.model()
            if form_validated:
                return self.response_add(request, form)

        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
            form = Form(initial=initial)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.prepopulated_fields, self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': "_popup" in request.REQUEST,
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = self.model._meta

        msg = _('%(name)s was submitted successfully.') % {
            'name': force_unicode(opts.verbose_name),
        }

        if "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)

        self.message_user(request, msg)

        post_url = '../../'
        return HttpResponseRedirect(post_url)
