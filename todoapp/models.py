# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils.timezone import get_current_timezone
# Create your models here.
class Todolist(models.Model):
	task = models.CharField(max_length=200, null=True)
	priority = models.IntegerField(default= '3')
	
	

