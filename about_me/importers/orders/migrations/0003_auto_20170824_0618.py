# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-24 04:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20170823_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 25, 6, 18, 41, 304263)),
        ),
    ]
