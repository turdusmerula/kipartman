# Generated by Django 3.1 on 2020-09-22 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_part_new_footprint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='footprint',
        ),
    ]