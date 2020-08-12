# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 13:36
from __future__ import unicode_literals

from django.db import migrations
from api.models import UnitPrefix

# Add default values to database

# create default values for units
def load_units(apps, schema_editor):
    Unit = apps.get_model("api", "Unit")
    
    units = [
        Unit(name='Ampere', symbol='A'),
        Unit(name='Ampere Hour', symbol='Ah'),
        Unit(name='Becquerel', symbol='Bq'),
        Unit(name='byte', symbol='B'),
        Unit(name='Candela', symbol='cd'),
        Unit(name='Celsius', symbol='°C'),
        Unit(name='Coulomb', symbol='C'),
        Unit(name='degree', symbol='°'),
        Unit(name='Farad', symbol='F'),
        Unit(name='Gram', symbol='g'),
        Unit(name='Gray', symbol='Gy'),
        Unit(name='Henry', symbol='H'),
        Unit(name='Hertz', symbol='Hz'),
        Unit(name='Joule', symbol='J'),
        Unit(name='Katal', symbol='kat'),
        Unit(name='Kelvin', symbol='K'),
        Unit(name='Lumen', symbol='lm'),
        Unit(name='Lux', symbol='lx'),
        Unit(name='Meter', symbol='m'),
        Unit(name='Mol', symbol='mol'),
        Unit(name='Newton', symbol='N'),
        Unit(name='Ohm', symbol='Ω'),
        Unit(name='Pascal', symbol='Pa'),
        Unit(name='ppm/degC', symbol='ppm/°C'),
        Unit(name='Second', symbol='s'),
        Unit(name='Siemens', symbol='S'),
        Unit(name='Sievert', symbol='Sv'),
        Unit(name='Tesla', symbol='T'),
        Unit(name='Volt', symbol='V'),
        Unit(name='Watt', symbol='W'),
        Unit(name='Weber', symbol='Wb'),
    ]
    
    for unit in units:
        try:
            Unit.objects.get(name=unit.name)
        except Unit.DoesNotExist:
            print("Add ", unit.name)
            unit.save()

# create default values for unit prefixes
def load_unit_prefixes(apps, schema_editor):
    UnitPrefix = apps.get_model("api", "UnitPrefix")

    prefixes = [
        UnitPrefix(name='yotta', symbol='Y', power='1E24'),
        UnitPrefix(name='zetta', symbol='Z', power='1E21'),
        UnitPrefix(name='exa', symbol='E', power='1E18'),
        UnitPrefix(name='peta', symbol='P', power='1E15'),
        UnitPrefix(name='tera', symbol='T', power='1E12'),
        UnitPrefix(name='giga', symbol='G', power='1E9'),
        UnitPrefix(name='mega', symbol='M', power='1E6'),
        UnitPrefix(name='kilo', symbol='k', power='1E3'),
        UnitPrefix(name='hecto', symbol='h', power='1E2'),
        UnitPrefix(name='deca', symbol='da', power='1E1'),
        UnitPrefix(name='-', symbol='', power='1E0'),
        UnitPrefix(name='deci', symbol='d', power='1E-1'),
        UnitPrefix(name='centi', symbol='c', power='1E-2'),
        UnitPrefix(name='milli', symbol='m', power='1E-3'),
        UnitPrefix(name='micro', symbol='µ', power='1E-6'),
        UnitPrefix(name='nano', symbol='n', power='1E-9'),
        UnitPrefix(name='pico', symbol='p', power='1E-12'),
        UnitPrefix(name='femto', symbol='f', power='1E-15'),
        UnitPrefix(name='atto', symbol='a', power='1E-18'),
        UnitPrefix(name='yocto', symbol='y', power='1E-24'),
        UnitPrefix(name='kibi', symbol='Ki', power='1024'),
        UnitPrefix(name='mebi', symbol='Mi', power='1024^2'),
        UnitPrefix(name='gibi', symbol='Gi', power='1024^3'),
        UnitPrefix(name='tebi', symbol='Ti', power='1024^4'),
        UnitPrefix(name='pebi', symbol='Pi', power='1024^5'),
        UnitPrefix(name='exbi', symbol='Ei', power='1024^6'),
        UnitPrefix(name='zebi', symbol='Zi', power='1024^7'),
        UnitPrefix(name='yobi', symbol='Yi', power='1024^8'),
    ]
    
    for prefix in prefixes:
        try:
            UnitPrefix.objects.get(name=prefix.name)
        except UnitPrefix.DoesNotExist:
            print("Add ", prefix.name)
            prefix.save()

# create default values for units
def load_currencies(apps, schema_editor):
    Currency = apps.get_model("api", "Currency")

    currencies = [
        Currency(name='EUR', symbol='€', base='EUR', ratio=1),
        Currency(name='AUD', symbol='AUD', base='EUR', ratio=1.5382),
        Currency(name='BGN', symbol='BGN', base='EUR', ratio=1.9558),
        Currency(name='BRL', symbol='BRL', base='EUR', ratio=3.9171),
        Currency(name='CAD', symbol='CAD', base='EUR', ratio=1.507),
        Currency(name='CHF', symbol='CHF', base='EUR', ratio=1.1669),
        Currency(name='CNY', symbol='CNY', base='EUR', ratio=7.8022),
        Currency(name='CZK', symbol='CZK', base='EUR', ratio=25.678),
        Currency(name='DKK', symbol='DKK', base='EUR', ratio=7.4443),
        Currency(name='GBP', symbol='GBP', base='EUR', ratio=0.88253),
        Currency(name='HKD', symbol='HKD', base='EUR', ratio=9.2223),
        Currency(name='HRK', symbol='HRK', base='EUR', ratio=7.5465),
        Currency(name='HUF', symbol='HUF', base='EUR', ratio=313.43),
        Currency(name='IDR', symbol='IDR', base='EUR', ratio=16029.0),
        Currency(name='ILS', symbol='ILS', base='EUR', ratio=4.1634),
        Currency(name='INR', symbol='INR', base='EUR', ratio=75.608),
        Currency(name='JPY', symbol='JPY', base='EUR', ratio=132.45),
        Currency(name='KRW', symbol='KRW', base='EUR', ratio=1284.7),
        Currency(name='MXN', symbol='MXN', base='EUR', ratio=22.628),
        Currency(name='MYR', symbol='MYR', base='EUR', ratio=4.8163),
        Currency(name='NOK', symbol='NOK', base='EUR', ratio=9.7828),
        Currency(name='NZD', symbol='NZD', base='EUR', ratio=1.6803),
        Currency(name='PHP', symbol='PHP', base='EUR', ratio=59.528),
        Currency(name='PLN', symbol='PLN', base='EUR', ratio=4.2167),
        Currency(name='RON', symbol='RON', base='EUR', ratio=4.6332),
        Currency(name='RUB', symbol='RUB', base='EUR', ratio=69.504),
        Currency(name='SEK', symbol='SEK', base='EUR', ratio=9.9583),
        Currency(name='SGD', symbol='SGD', base='EUR', ratio=1.5897),
        Currency(name='THB', symbol='THB', base='EUR', ratio=38.375),
        Currency(name='TRY', symbol='TRY', base='EUR', ratio=4.5603),
        Currency(name='USD', symbol='$', base='EUR', ratio=1.1806),
        Currency(name='ZAR', symbol='ZAR', base='EUR', ratio=15.781),
    ]
    
    for currency in currencies:
        try:
            Currency.objects.get(name=currency.name)
        except Currency.DoesNotExist:
            print("Add ", currency.name)
            currency.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_currency'),
    ]

    operations = [
        migrations.RunPython(load_units),
        migrations.RunPython(load_unit_prefixes),
        migrations.RunPython(load_currencies)
    ]