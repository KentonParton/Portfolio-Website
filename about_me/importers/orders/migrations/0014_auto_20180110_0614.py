# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-01-10 04:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20180109_0244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 11, 6, 14, 1, 410780)),
        ),
    ]
