# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from todoapp.models import Todolist, Registration
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.
def registration_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name', 'User name is not given')
        emailid = request.POST.get('email_id', 'emailid not defined')
        passwd= request.POST.get('passwd','not given')
        try:
            a = Registration(user_name = user_name, email_id = emailid, password= passwd)
            a.save() 
        except IntegrityError:
            t = "This user already exists"
            return render(request,"registration.html", {'text': t})
        t = "You have succesfully registered" 
        return render(request,'registration.html', {'text':t})  
    return render(request, 'registration.html')

def login_page(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id', None)
        passwd= request.POST.get('passwd',None)
        print request.POST
        print email_id
        print passwd
        try:
            email_val= Registration.objects.get(email_id = email_id, password = passwd)
            print email_val
            request.session['user_login'] = email_val.id
            return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            t = "Email or password is not valid. Please try again" 
            return render(request,'login.html', {'text':t})     
    return render(request, 'login.html')

def logout(request):
    try:
        del request.session['user_login']
    except KeyError:
        pass
    t="You are logged out"
    return render(request, 'login.html', {'text':t})


def login_valid(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id', None)
        passwd= request.POST.get('passwd',None)
        print email_id
        print passwd
        try:
            email_val= Registration.objects.get(email_id = email_id, password = passwd)
            print email_val
            return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            t = "Email or password is not valid" 
            return render(request,'login.html', {'text':t})     
    return HttpResponseRedirect('/')

def test(request):
    print request.session.get('user_login', None)
    if not request.session.get('user_login', None):
        return HttpResponseRedirect('/login')

    #if 'user_login' in request.session:
    #    del request.session['user_login']
    #    return HttpResponseRedirect('/registration')

    if request.method == 'POST':
        task_data = request.POST.get('task_data', 'Task not defined')
        priority = request.POST.get('priority', 3)
        task_date = request.POST.get('task_date',None)
        if task_date == '':
            task_date = None
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

