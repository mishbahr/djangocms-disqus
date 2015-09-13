# -*- coding: utf-8 -*-

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class DjangoCMSDisqusConf(AppConf):
    PLUGIN_MODULE = _('Generic')
    PLUGIN_NAME = _('Disqus Comments')
    PLUGIN_TEMPLATE = 'djangocms_disqus/default.html'
    USER_MODEL_EMAIL_FIELD = 'email'
    HASHIDS_SALT = settings.SECRET_KEY
    USE_GRAVATAR = True
    ENABLE_SSO = False
    LOGIN_URL = settings.LOGIN_URL
    LOGOUT_URL = settings.LOGOUT_URL

    LOADING_CHOICES = (
        ('immediately', _('Immediately')),
        ('lazyload', _('Lazy Load')),
        ('click', _('On Click')),
    )

    class Meta:
        prefix = 'djangocms_disqus'
