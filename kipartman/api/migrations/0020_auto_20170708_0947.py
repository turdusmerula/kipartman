# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-08 09:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20170708_0939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='parts',
            new_name='childs',
        ),
    ]
