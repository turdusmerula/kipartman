# Generated by Django 4.0 on 2022-02-06 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_remove_part_metapart_part_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('request', models.TextField()),
                ('result', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='part',
            name='provider',
            field=models.TextField(choices=[('octopart', 'Octopart')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='partparameter',
            name='operator',
            field=models.TextField(choices=[('=', 'Eq'), ('!=', 'Ne'), ('>', 'Gt'), ('>=', 'Ge'), ('<', 'Mt'), ('<=', 'Me'), ('x, y', 'Range'), ('x, y, z', 'List')], default='=', null=True),
        ),
    ]