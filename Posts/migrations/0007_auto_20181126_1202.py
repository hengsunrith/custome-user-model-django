# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-26 05:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0006_auto_20181120_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 26, 5, 2, 0, 999936, tzinfo=utc)),
        ),
    ]
