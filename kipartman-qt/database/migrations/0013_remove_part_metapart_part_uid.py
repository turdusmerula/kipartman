# Generated by Django 4.0 on 2022-02-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_init_part_instance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='metapart',
        ),
        migrations.AddField(
            model_name='part',
            name='uid',
            field=models.TextField(blank=True, null=True),
        ),
    ]