# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aldryn_client import forms


class Form(forms.BaseForm):
    plugin_module = forms.CharField('Plugin module name', initial='Generic')
    plugin_name = forms.CharField('Plugin name', initial='Disqus Comments')
    plugin_template = forms.CharField('Plugin Template', required=False)
    disqus_public_key = forms.CharField(
        'Disqus Public Key',
        help_text='register new applications at https://disqus.com/api/applications/register/')
    disqus_secret_key = forms.CharField('Disqus Secret Key')

    def to_settings(self, data, settings):
        settings['DJANGOCMS_DISQUS_PLUGIN_MODULE'] = data['plugin_module']
        settings['DJANGOCMS_DISQUS_PLUGIN_NAME'] = data['plugin_name']

        plugin_template = data.get('plugin_template', '')
        if plugin_template:
            settings['DJANGOCMS_DISQUS_PLUGIN_TEMPLATE'] = plugin_template

        settings['CONNECTED_ACCOUNTS_DISQUS_CONSUMER_KEY'] = data['disqus_public_key']
        settings['CONNECTED_ACCOUNTS_DISQUS_CONSUMER_SECRET'] = data['disqus_secret_key']

        settings['MIDDLEWARE_CLASSES'].append('djangocms_disqus.middleware.DisqusMiddleware')

        return settings

