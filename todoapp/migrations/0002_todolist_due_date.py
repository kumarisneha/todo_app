# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 14:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
