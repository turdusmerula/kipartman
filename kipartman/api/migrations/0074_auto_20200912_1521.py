# Generated by Django 3.1 on 2020-09-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_auto_20200911_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library',
            old_name='mtime',
            new_name='mtime_lib',
        ),
        migrations.AddField(
            model_name='library',
            name='mtime_dcm',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
