# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-10 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20170810_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartStorages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('part', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='storages', to='api.Part')),
            ],
        ),
        migrations.RenameModel(
            old_name='PartStockHistory',
            new_name='PartStorageHistory',
        ),
        migrations.RemoveField(
            model_name='partstock',
            name='location',
        ),
        migrations.RemoveField(
            model_name='partstock',
            name='part',
        ),
        migrations.AddField(
            model_name='storage',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='PartStock',
        ),
        migrations.AddField(
            model_name='partstorages',
            name='storage',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.Storage'),
        ),
    ]
