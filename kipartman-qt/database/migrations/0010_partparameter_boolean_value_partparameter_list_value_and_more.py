# Generated by Django 4.0 on 2022-01-25 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_rename_value_partparameter_float_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partparameter',
            name='boolean_value',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='partparameter',
            name='list_value',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='value_type',
            field=models.TextField(choices=[('integer', 'Integer'), ('float', 'Float'), ('text', 'Text'), ('boolean', 'Boolean'), ('list', 'List')], default='float'),
        ),
    ]
