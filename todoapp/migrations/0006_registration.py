# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_todolist_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50, null=True)),
                ('email_id', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
