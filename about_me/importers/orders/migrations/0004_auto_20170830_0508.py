# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-30 03:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20170824_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 31, 5, 8, 6, 43054)),
        ),
    ]
