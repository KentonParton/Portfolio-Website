# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-01-17 06:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20180115_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 18, 0, 28, 16, 774165)),
        ),
    ]
