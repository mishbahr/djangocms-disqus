#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangocms_disqus

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_disqus.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='djangocms-disqus',
    version=version,
    description="""Disqus intergration for your django-cms powered site with options for Single Sign-On (SSO), lazy loading, analytics and more.""",
    long_description=readme,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/djangocms-disqus',
    packages=[
        'djangocms_disqus',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf',
        'django-connected',
        'django-cms>=3.0',
        'hashids',
        'requests>=2.7.0',
        'disqus-python',
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangocms-disqus, django-cms, cmsplugin-disqus, disqus sso, lazyload',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
