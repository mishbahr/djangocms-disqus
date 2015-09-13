# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

import requests
from connected_accounts.models import Account
from disqusapi import APIError, DisqusAPI, InvalidAccessToken
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids
from requests.exceptions import HTTPError

from .conf import settings
from .exceptions import DisqusAPIError


def get_model_tuple(model):
    """
    Takes a model or a string of the form "app_label.ModelName" and returns a
    corresponding ("app_label", "modelname") tuple.
    """
    if isinstance(model, six.string_types):
        app_label, model_name = model.split('.')
        model_tuple = app_label, model_name.lower()
    else:
        model_tuple = model._meta.app_label, model._meta.object_name.lower()
    return model_tuple


def int_to_hashid(i, min_length=11, salt=settings.DJANGOCMS_DISQUS_HASHIDS_SALT):
    hashids = Hashids(salt, min_length=min_length)
    return hashids.encode(i)


def hashid_to_int(hashid, min_length=11, salt=settings.DJANGOCMS_DISQUS_HASHIDS_SALT):
    hashids = Hashids(salt, min_length=min_length)

    try:
        return hashids.decode(hashid)[0]
    except IndexError:
        pass


def calculate_gravatar_hash(email):
    # Calculate the email hash
    enc_email = email.strip().lower().encode('utf-8')
    email_hash = hashlib.md5(enc_email).hexdigest()
    return email_hash


def get_gravatar_url(email, secure=False):
    """
    Builds a url to a gravatar from an email address.
    """
    if secure:
        url_base = 'https://secure.gravatar.com/'
    else:
        url_base = 'http://www.gravatar.com/'

    # Calculate the email hash
    email_hash = calculate_gravatar_hash(email)

    url = '{base}avatar/{hash}.jpg'.format(base=url_base, hash=email_hash)

    params = {
        'size': 256,
        'default': '404',
        'rating': 'g',
    }

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
    except HTTPError:
        pass
    else:
        return resp.url


def get_forums_list(account_id):
    public_key = settings.CONNECTED_ACCOUNTS_DISQUS_CONSUMER_KEY
    secret_key = settings.CONNECTED_ACCOUNTS_DISQUS_CONSUMER_SECRET
    disqus = DisqusAPI(secret_key=secret_key, public_key=public_key)

    forums = []

    try:
        connected_account = Account.objects.get(pk=account_id)
    except Account.DoesNotExist:
        raise DisqusAPIError(_('Account does not exist!'))
    else:
        try:
            forums_list = disqus.users.listForums(access_token=connected_account.get_token())
        except (APIError, InvalidAccessToken) as e:
            raise DisqusAPIError(e.message)
        else:
            for forum in forums_list:
                shortname = forum['id']
                label_from_instance = '{name} ({shortname})'.format(
                    name=forum['name'], shortname=shortname)
                forums.append((shortname, label_from_instance))

    return forums
