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
        priority = request.POST.get('priority', 3)
        task_date = request.POST.get('task_date',None)
        a = Todolist(task = task_data, priority=priority, due_date=task_date)
        a.save()
        
    sample = {'object_list': Todolist.objects.all().order_by('priority')}
    return render(request, 'index.html', sample)

def delete_item(request, id):
    obj=Todolist.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/')

def delete_all(request):
    obj=Todolist.objects.all()
    for i in obj:
        i.delete()
    return HttpResponseRedirect('/')

def update_list(request, id):
    obj=Todolist.objects.get(id=id)
    context={'xyz': obj}
    return render(request, 'update.html', context)

def newpage(request, id):
    if request.method == 'POST':
        name=request.POST.get("name", "Task is updated")
        pri_val= request.POST.get('priority','3')
        obj = Todolist.objects.get(id=id)
        obj.priority= pri_val
        obj.task=name
        obj.save()
        return HttpResponseRedirect('/')

