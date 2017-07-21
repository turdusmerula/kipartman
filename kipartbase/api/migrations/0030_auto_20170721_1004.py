# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-21 10:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20170720_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, default='')),
                ('comment', models.TextField(blank=True, default='')),
                ('snapeda', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModelCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, default='')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ModelCategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='model',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.ModelCategory'),
        ),
        migrations.AddField(
            model_name='model',
            name='childs',
            field=models.ManyToManyField(blank=True, related_name='model_childs', to='api.Model'),
        ),
        migrations.AddField(
            model_name='model',
            name='image',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_image', to='api.File'),
        ),
        migrations.AddField(
            model_name='model',
            name='model',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='model_file', to='api.File'),
        ),
    ]
