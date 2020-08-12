# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20170709_2338'),
    ]

    operations = [
        migrations.RenameModel('PartDistributor', 'PartOffer'),
        migrations.AlterField(
            model_name='partmanufacturer',
            name='part',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='manufacturers', to='api.Part'),
        ),
        migrations.AlterField(
            model_name='partoffer',
            name='part',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='api.Part'),
        ),
    ]
