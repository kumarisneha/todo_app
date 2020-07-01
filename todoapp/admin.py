# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Registration, Todolist

# Register your models here.
admin.site.register(Registration)
admin.site.register(Todolist)