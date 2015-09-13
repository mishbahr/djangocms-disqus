# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.models import CMSPlugin
from connected_accounts.fields import AccountField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .conf import settings


@python_2_unicode_compatible
class Disqus(CMSPlugin):
    account = AccountField(
        'disqus', verbose_name=_('Connected Account'),
        help_text=_('Select a connected Disqus account or connect to a new account.'))

    shortname = models.CharField(
        _('Shortname'), max_length=150,
        help_text=_('Select a website Or register a new one on the Disqus website. '
                    'https://disqus.com/admin/signup/'))
    enable_sso = models.BooleanField(
        _('Enable Single Sign-On'), default=False,
        help_text=_('Allows users to log in to Disqus via your site.'))
    load_event = models.CharField(
        _('Load Disqus'), max_length=100,
        default=settings.DJANGOCMS_DISQUS_LOADING_CHOICES[0][0],
        choices=settings.DJANGOCMS_DISQUS_LOADING_CHOICES)
    site_name = models.CharField(
        _('Site Name'), max_length=100, blank=True,
        help_text=_('Used for the SSO login button.'))
    button_text = models.CharField(
        _('Button Text'), max_length=100, blank=True,
        help_text=_('By default it will be "Load Comments..."'))

    def __str__(self):
        return '{shortname}.disqus.com'.format(shortname=self.shortname)

    def moderate(self):
        template = """
        <a href="https://{shortname}.disqus.com/admin/moderate/" target="_blank">
            {link_text}
        </a>
        """
        return template.format(
            shortname=self.shortname,
            link_text=_('Go to Disqus Moderation'))
    moderate.allow_tags = True
