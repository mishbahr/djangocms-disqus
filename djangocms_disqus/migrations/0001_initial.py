# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from connected_accounts.fields import AccountField

from ..conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('connected_accounts', '__latest__'),
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disqus',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('shortname', models.CharField(help_text='Select a website Or register a new one on the Disqus website. https://disqus.com/admin/signup/', max_length=150, verbose_name='Shortname')),
                ('enable_sso', models.BooleanField(default=False, help_text='Allows users to log in to Disqus via your site.', verbose_name='Enable Single Sign-On')),
                ('load_event', models.CharField(default=settings.DJANGOCMS_DISQUS_LOADING_CHOICES[0][0], max_length=100, verbose_name='Load Disqus', choices=settings.DJANGOCMS_DISQUS_LOADING_CHOICES)),
                ('site_name', models.CharField(help_text='Used for the SSO login button.', max_length=100, verbose_name='Site Name', blank=True)),
                ('button_text', models.CharField(help_text='By default it will be "Load Comments..."', max_length=100, verbose_name='Button Text', blank=True)),
                ('account', AccountField(verbose_name='Connected Account', to='connected_accounts.Account', provider='disqus', help_text='Select a connected Disqus account or connect to a new account.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
