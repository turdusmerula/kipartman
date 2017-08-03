# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-20 13:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_auto_20170720_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footprint',
            name='footprint',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='footprint', to='api.File'),
        ),
        migrations.AlterField(
            model_name='footprint',
            name='image',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='image', to='api.File'),
        ),
    ]