# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-21 00:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20171021_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 22, 2, 11, 39, 382763)),
        ),
    ]
