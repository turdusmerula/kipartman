# Generated by Django 4.0 on 2022-02-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_requestcache_part_provider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='findchips',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='parameter',
            name='octopart',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='parameter',
            name='values',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]