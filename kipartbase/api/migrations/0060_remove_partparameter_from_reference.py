# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-25 23:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0059_auto_20181224_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partparameter',
            name='from_reference',
        ),
    ]
