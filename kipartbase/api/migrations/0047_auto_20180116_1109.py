# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-16 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_versionedfile_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versionedfile',
            name='metadata',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
