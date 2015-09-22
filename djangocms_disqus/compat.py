import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site


class JsonResponse(HttpResponse):

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                            'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder)
        super(JsonResponse, self).__init__(content=data, **kwargs)
