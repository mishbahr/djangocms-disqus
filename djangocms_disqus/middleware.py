import base64
import hashlib
import hmac
import json
import time

from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.template.loader import render_to_string
from django.utils import translation

from .compat import get_current_site
from .conf import settings
from .utils import get_gravatar_url, get_model_tuple, int_to_hashid

LOGIN_SUCCESS_VAR = 'disqus-login-success'


class Disqus(object):

    public_key = settings.CONNECTED_ACCOUNTS_DISQUS_CONSUMER_KEY
    secret_key = settings.CONNECTED_ACCOUNTS_DISQUS_CONSUMER_SECRET
    enable_sso = settings.DJANGOCMS_DISQUS_ENABLE_SSO
    language_code = translation.get_language()

    def __init__(self, request):
        self.request = request
        self.current_site = get_current_site(self.request)
        self.timestamp = int(time.time())
        self.obj = None
        self._identifier = None
        self._title = None
        self._category_id = None
        self._url = None

    def set_object(self, obj):
        self.obj = obj

    def get_object_model(self):
        if self.obj:
            app_label, model_name = get_model_tuple(self.obj.__class__)
            return '{app_label}/{model_name}'.format(
                app_label=app_label,
                model_name=model_name).lower()
        return ''

    def get_object_hashid(self):
        if self.obj:
            return int_to_hashid(self.obj.pk, min_length=11, salt='disqus_identifier')
        return ''

    def set_identifier(self, identifier):
        self._identifier = identifier

    def get_identifier(self):
        if not self._identifier and self.obj:
            self._identifier = '/{model}/{id}/'.format(
                model=self.get_object_model(), id=self.get_object_hashid())

        if self._identifier:
            return self._identifier

        return self.request.path_info

    identifier = property(get_identifier, set_identifier)

    def set_title(self, title):
        self._title = title

    def get_title(self):
        if self._title:
            return self._title
        return 'No title'

    title = property(get_title, set_title)

    def set_category_id(self, category_id):
        self._category_id = category_id

    def get_category_id(self):
        if self._category_id:
            return self._category_id
        return ''

    category_id = property(get_category_id, set_category_id)

    def set_url(self, url):
        self._url = url

    def get_url(self):
        if self._url:
            return self.request.build_absolute_uri(location=self._url)
        return self.request.build_absolute_uri(location=self.request.path_info)

    url = property(get_url, set_url)

    def get_user_data(self):
        user = {}
        if hasattr(self.request, 'user'):
            user_obj = self.request.user
            if user_obj.is_authenticated():
                user.update({
                    'id': int_to_hashid(user_obj.pk, min_length=11, salt='disqus_user_id'),
                    'username': getattr(user_obj, get_user_model().USERNAME_FIELD),
                    'email': getattr(user_obj, settings.DJANGOCMS_DISQUS_USER_MODEL_EMAIL_FIELD),
                })

                if settings.DJANGOCMS_DISQUS_USE_GRAVATAR:
                    avatar_url = get_gravatar_url(user.get('email'), secure=self.request.is_secure)
                    if avatar_url:
                        user['avatar'] = avatar_url

        return user

    def get_b64encoded_user_data(self):
        return base64.b64encode(json.dumps(self.get_user_data()))

    def generate_hmac_sha1_signature(self):
        return hmac.HMAC(
            self.secret_key,
            '{user_data} {timestamp}'.format(
                user_data=self.get_b64encoded_user_data(),
                timestamp=self.timestamp),
            hashlib.sha1).hexdigest()

    def get_sso_auth(self):
        return '{user_data} {hmac} {timestamp}'.format(
            user_data=self.get_b64encoded_user_data(),
            hmac=self.generate_hmac_sha1_signature(),
            timestamp=self.timestamp,
        )

    def get_login_url(self):
        login_url = self.request.build_absolute_uri(
            location=settings.DJANGOCMS_DISQUS_LOGIN_URL)

        next_page = '{url}?{login_success}=1'.format(
            url=self.request.path_info,
            login_success=LOGIN_SUCCESS_VAR)

        return '{login_url}?{redirect_field}={next}'.format(
            login_url=login_url,
            redirect_field=REDIRECT_FIELD_NAME,
            next=next_page,
        )

    def get_logout_url(self):
        logout_url = self.request.build_absolute_uri(
            location=settings.DJANGOCMS_DISQUS_LOGOUT_URL)

        return '{logout_url}?{redirect_field}={next}'.format(
            logout_url=logout_url,
            redirect_field=REDIRECT_FIELD_NAME,
            next=self.request.path_info,
        )


class DisqusMiddleware(object):
    """
    Middleware to set up Disqus SSO.
    """

    def process_request(self, request):
        request.disqus = Disqus(request)
        current_page = getattr(request, 'current_page', None)

        if current_page:
            draft_page = current_page.get_draft_object()
            request.disqus.set_object(draft_page)
            request.disqus.set_title(current_page.get_title())

    def process_response(self, request, response):
        if LOGIN_SUCCESS_VAR in request.GET:
            login_success = render_to_string(template_name='djangocms_disqus/login_success.html')
            response.content = login_success
            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)

        return response
