from django.core.urlresolvers import reverse
from django.forms import Select
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from djangocms_disqus.exceptions import DisqusAPIError

from .models import Disqus
from .utils import get_forums_list, get_model_tuple


class SelectShortnameWidget(Select):
    model = Disqus
    template = 'djangocms_disqus/admin/shortname_widget_wrapper.html'

    def __init__(self, obj, admin_site, attrs=None, choices=()):
        self.obj = obj
        self.admin_site = admin_site
        super(SelectShortnameWidget, self).__init__(attrs=attrs, choices=choices)

    def render(self, name, value, attrs=None, choices=(('', '---------'), )):
        if self.obj:
            try:
                choices = get_forums_list(self.obj.account.pk)
            except DisqusAPIError:
                pass

        widget = super(SelectShortnameWidget, self).render(
            name, value, attrs=attrs, choices=choices)

        if value is None:
            value = ''

        app_label, model_name = get_model_tuple(self.model)
        url_name = 'admin:{app_label}_{model_name}_list_forums'.format(
            app_label=app_label, model_name=model_name)

        context = {
            'widget': widget,
            'name': name,
            'value': value,
            'ajax_url': reverse(url_name, current_app=self.admin_site)
        }
        return mark_safe(render_to_string(self.template, context))
