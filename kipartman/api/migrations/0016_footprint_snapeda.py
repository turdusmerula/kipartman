# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-20 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20170614_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='footprint',
            name='snapeda',
            field=models.TextField(blank=True, null=True),
        ),
    ]
