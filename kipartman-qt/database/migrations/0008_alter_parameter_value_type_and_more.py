# Generated by Django 4.0 on 2022-01-21 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_remove_partparameter_prefix_partparameter_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value_type',
            field=models.TextField(choices=[('integer', 'Integer'), ('float', 'Float'), ('text', 'Text')], default='float'),
        ),
        migrations.AlterField(
            model_name='partparameter',
            name='operator',
            field=models.TextField(choices=[('=', 'Eq'), ('!=', 'Ne'), ('>', 'Gt'), ('>=', 'Ge'), ('<', 'Mt'), ('<=', 'Me'), ('f=', 'Func')], default='=', null=True),
        ),
        migrations.AlterField(
            model_name='partparameter',
            name='unit',
            field=models.TextField(null=True),
        ),
    ]
