# Generated by Django 3.1 on 2020-09-20 09:39

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('api', '0077_auto_20200913_2029'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LibrarySymbol',
            new_name='KicadSymbol'
        ),
        migrations.RenameModel(
            old_name='Library',
            new_name='KicadSymbolLibrary'
        ),
    ]