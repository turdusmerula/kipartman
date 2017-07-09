# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-05 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170605_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partdistributor',
            name='distributor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Distributor'),
        ),
    ]