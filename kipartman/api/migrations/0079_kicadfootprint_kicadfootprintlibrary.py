# Generated by Django 3.1 on 2020-09-20 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0078_auto_20200920_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='KicadFootprintLibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField(blank=True, default='')),
                ('mtime_lib', models.FloatField()),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='KicadFootprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('content', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('library', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='footprints', to='api.kicadfootprintlibrary')),
            ],
        ),
    ]
