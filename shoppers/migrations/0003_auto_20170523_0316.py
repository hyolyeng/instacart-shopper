# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 03:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppers', '0002_auto_20170523_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Phone number must contain only digits, of length 9-15', regex='^\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='application',
            name='zipcode',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Zip code should be 5 digits. eg. 94085', regex='^\\d{5}$')]),
        ),
    ]
