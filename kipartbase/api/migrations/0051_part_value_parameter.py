# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20180422_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='value_parameter',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='value_parameter', to='api.PartParameter'),
        ),
    ]