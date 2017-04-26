# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from todoapp.models import Todolist

# Create your views here.
def test(request):
    if request.method == 'POST':
        task_data = request.POST.get('task_data', 'Task not defined')
        a = Todolist(task = task_data)
        a.save()
        
    sample = {'object_list': Todolist.objects.all()}
    return render(request, 'test.html', sample)

def delete_item(request, id):
    obj=Todolist.objects.get(id=id)
    obj.delete()
    
    return HttpResponseRedirect('/')

def delete_all(request):
    obj=Todolist.objects.all()
    for i in obj:
        i.delete()
    return HttpResponseRedirect('/')

