=============================
djangocms-disqus
=============================

.. image:: http://img.shields.io/travis/mishbahr/djangocms-disqus.svg?style=flat-square
    :target: https://travis-ci.org/mishbahr/djangocms-disqus/

.. image:: http://img.shields.io/pypi/v/djangocms-disqus.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-disqus/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/djangocms-disqus.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-disqus/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/djangocms-disqus.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-disqus/
    :alt: License

.. image:: http://img.shields.io/coveralls/mishbahr/djangocms-disqus.svg?style=flat-square
  :target: https://coveralls.io/r/mishbahr/djangocms-disqus?branch=master

Disqus intergration for your django-cms powered site with options for Single Sign-On (SSO), lazy loading, analytics and more.

This project requires `django-connected <https://github.com/mishbahr/django-connected>`_ and ``django-cms`` v3.0 or
higher to be properly installed and configured. When installing the ``djangocms-disqus`` using pip, ``django-connected`` will also be installed automatically.


Quickstart
----------

1. Install ``djangocms-disqus``::

    pip install djangocms-disqus

2. Add ``djangocms_disqus`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'connected_accounts',
        'connected_accounts.providers',
        'djangocms_disqus',
        ...
    )

3. To enable ``Disqus`` as a provider for ``django-connected`` (register new applications at https://disqus.com/api/applications/register/)::

    CONNECTED_ACCOUNTS_DISQUS_CONSUMER_KEY = '<disqus_secret_key>'
    CONNECTED_ACCOUNTS_DISQUS_CONSUMER_SECRET = '<disqus_public_key>'

4. Sync database (requires south>=1.0.1 if you are using Django 1.6.x)::

    python manage.py migrate

5. Add the ``DisqusMiddleware`` to ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        ...
        'djangocms_disqus.middleware.DisqusMiddleware',
        ...
    )

Preview
-------

.. image:: http://mishbahr.github.io/assets/djangocms-disqus/thumbnail/djangocms-disqus-001.png
  :target: http://mishbahr.github.io/assets/djangocms-disqus/djangocms-disqus-001.png
  :width: 768px
  :align: center


.. image:: http://mishbahr.github.io/assets/djangocms-disqus/thumbnail/djangocms-disqus-002.png
  :target: http://mishbahr.github.io/assets/djangocms-disqus/djangocms-disqus-002.png
  :width: 768px
  :align: center


You may also like...
--------------------

* djangocms-forms — https://github.com/mishbahr/djangocms-forms
* djangocms-gmaps — https://github.com/mishbahr/djangocms-gmaps
* djangocms-instagram — https://github.com/mishbahr/djangocms-instagram
* djangocms-responsive-wrapper — https://github.com/mishbahr/djangocms-responsive-wrapper
* djangocms-twitter2 — https://github.com/mishbahr/djangocms-twitter2
* djangocms-youtube — https://github.com/mishbahr/djangocms-youtube