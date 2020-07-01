# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils.timezone import get_current_timezone
# Create your models here.
class Registration(models.Model):
    user_name= models.CharField(max_length = 50)
    email_id = models.CharField(max_length = 50, unique=True)   
    password= models.CharField(max_length = 50)
    email_verified = models.BooleanField(default=False)
    email_active = models.BooleanField(default=True)
    
class Todolist(models.Model):
	task = models.CharField(max_length=200, null=True)
	priority = models.IntegerField(default= '3')
	due_date = models.DateTimeField(null=True)
	person = models.ForeignKey(Registration, blank=True, null=True, on_delete=models.SET_NULL)


	
	

