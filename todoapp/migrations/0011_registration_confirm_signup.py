# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0010_todolist_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='confirm_signup',
            field=models.BooleanField(default=False),
        ),
    ]