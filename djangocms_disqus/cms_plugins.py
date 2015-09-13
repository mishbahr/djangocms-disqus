# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from django.conf.urls import patterns, url
from django.contrib import admin
from django.utils.encoding import force_text

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from connected_accounts.admin import ConnectedAccountAdminMixin

from .conf import settings
from .exceptions import DisqusAPIError
from .models import Disqus
from .utils import get_forums_list, get_model_tuple
from .widgets import SelectShortnameWidget

try:
    from django.http import JsonResponse
except ImportError:
    from .compat import JsonResponse


class DisqusPlugin(ConnectedAccountAdminMixin, CMSPluginBase):
    model = Disqus
    cache = False
    module = settings.DJANGOCMS_DISQUS_PLUGIN_MODULE
    name = settings.DJANGOCMS_DISQUS_PLUGIN_NAME
    render_template = settings.DJANGOCMS_DISQUS_PLUGIN_TEMPLATE
    readonly_fields = ('moderate', )

    fieldsets = (
        (None, {
            'fields': ('account', 'shortname', )
        }),
        (None, {
            'fields': ('load_event', 'button_text', )
        })
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(DisqusPlugin, self).get_fieldsets(request, obj=obj)
        if settings.DJANGOCMS_DISQUS_ENABLE_SSO:
            fieldsets = fieldsets + (
                (None, {
                    'fields': ('enable_sso', 'site_name', )
                }),
            )
        if obj:
            fieldsets = fieldsets + (
                (None, {
                    'fields': ('moderate', )
                }),
            )
        return fieldsets

    def get_plugin_urls(self):
        app_label, model_name = get_model_tuple(self.model)
        return patterns(
            '',
            url(r'^list/forums/$',
                admin.site.admin_view(self.list_forums),
                name='{app_label}_{model_name}_list_forums'.format(
                    app_label=app_label, model_name=model_name)),
        )

    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, obj=obj)
        return super(DisqusPlugin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        obj = kwargs.pop('obj', None)
        if db_field.name == 'shortname':
            kwargs['widget'] = SelectShortnameWidget(obj, self.admin_site)
            return db_field.formfield(**kwargs)
        return super(DisqusPlugin, self).formfield_for_dbfield(db_field, **kwargs)

    def list_forums(self, request):
        status_code = 200
        response = {}
        try:
            forums_list = get_forums_list(request.GET.get('account'))
        except DisqusAPIError as e:
            response['msg'] = force_text(e.message)
            status_code = 400
        else:
            response = dict(forums_list)

        return JsonResponse(response, status=status_code)

    class Media:
        css = {
            'all': ('css/djangocms_disqus/admin/djangocms_disqus.css',)
        }
        js = ('js/djangocms_disqus/admin/djangocms_disqus.js',)


plugin_pool.register_plugin(DisqusPlugin)
