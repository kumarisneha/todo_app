# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from todoapp.models import Todolist
import datetime
# Create your views here.
def test(request):
    if request.method == 'POST':
        task_data = request.POST.get('task_data', 'Task not defined')
        priority = request.POST.get('priority', 3)
        task_date = request.POST.get('task_date',None)
        if task_date:
            task_date=datetime.datetime.strptime(task_date, '%Y-%m-%d %H:%M')
        a = Todolist(task = task_data, priority = priority, due_date= task_date)
        a.save()  
    choose = request.GET.get('choose',1)
    if int(choose) == 2 :
        context={'todo_list': Todolist.objects.all().order_by('due_date')}
    else:
        context={'todo_list': Todolist.objects.all().order_by('priority')}     
    return render(request, 'index.html', context)

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
        update_date=request.POST.get("update_date", None)
        if update_date:
            update_date=datetime.datetime.strptime(update_date, '%Y-%m-%d %H:%M')
        obj = Todolist.objects.get(id=id)
        obj.priority= pri_val
        obj.task=name
        obj.due_date=update_date
        obj.save()
        return HttpResponseRedirect('/')

