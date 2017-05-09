# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from todoapp.models import Todolist, Registration
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from todo.celery import reverse, some_task

# from django.core.mail import send_mail
# send_mail('Django Mail', 'First message using django.', 'kumarisneha102@gmail.com', ['snehatezu@gmail.com'], fail_silently=False)
# Create your views here.
def registration_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name', None)
        emailid = request.POST.get('email_id', None)
        passwd= request.POST.get('passwd', None)
        if str(emailid) == '':
            emailid = None
        if str(user_name) == '':
            user_name = None
        if str(passwd) == '':
            passwd = None
        if not emailid or not user_name or not passwd:
            t = "Please fill all fields"
            return render(request,"registration.html", {'text': t})

        print user_name
        print emailid
        print passwd
        try:
            validate_email(emailid)
            try:
                a = Registration(user_name = user_name, email_id = emailid, password= passwd)
                a.save() 
            except IntegrityError:
                t = "This user already exists"
                return render(request,"registration.html", {'text': t})
            t = "You have succesfully registered" 
            return render(request,'registration.html', {'text':t})
        except ValidationError:
            t = "oops!!! wrong email"
            return render(request,"registration.html", {'text': t})                 
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

def home(request):
    print request.session.get('user_login', None)
    if not request.session.get('user_login', None):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        person_id = request.session.get('user_login', None)
        task_data = request.POST.get('task_data', 'Task not defined')
        priority = request.POST.get('priority', 3)
        task_date = request.POST.get('task_date',None)
        print priority
        print task_date
        if task_date.strip() == '':
            task_date = None
        if priority == 'Priority':
            priority = 3
        if task_date:
            task_date=datetime.datetime.strptime(task_date, '%Y-%m-%d %H:%M')
        a = Todolist(task = task_data, priority = priority, due_date= task_date, person_id= person_id)
        a.save()
    person_id = request.session.get('user_login', None)

    choose = request.GET.get('choose',1)
    if int(choose) == 2 :
        context={
            'todo_list': Todolist.objects.filter(person_id = person_id).order_by('due_date'),
            'username': Registration.objects.get(id=person_id).user_name,
            'user_id': Registration.objects.get(id=person_id).id,
            'user': Registration.objects.get(id=person_id).user_name.split(" ")[0],
            'emailid': Registration.objects.get(id=person_id).email_id,
            }
    else:
        context={
            'todo_list': Todolist.objects.filter(person_id = person_id).order_by('priority'),
            'username': Registration.objects.get(id=person_id).user_name,
            'user': Registration.objects.get(id=person_id).user_name.split(" ")[0],
            'emailid': Registration.objects.get(id=person_id).email_id,
            }     
    return render(request, 'index.html', context)

def delete_item(request, id):
    obj=Todolist.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/')

def delete_all(request):
    person_id = request.session.get('user_login', None)
    obj=Todolist.objects.filter(person_id = person_id)
    for i in obj:
        i.delete()
    return HttpResponseRedirect('/')

def update_list(request, id):
    person_id = request.session.get('user_login', None)
    try:
        obj=Todolist.objects.get(id = id, person_id = person_id)
    except:
        t = "Unauthorized access" 
        return render(request,'update.html', {'text':t})
    context={'xyz': obj}
    return render(request, 'update.html', context)

def newpage(request, id):
    if request.method == 'POST':
        name=request.POST.get("name", "Task is updated")
        pri_val= request.POST.get('priority','3')
        update_date=request.POST.get("update_date", None)
        if update_date == '':
            update_date = None
        if update_date:
            update_date=datetime.datetime.strptime(update_date, '%Y-%m-%d %H:%M')
        person_id = request.session.get('user_login', None)
        try:
            obj=Todolist.objects.get(id = id, person_id = person_id)
        except:
            t = "Unauthorized access" 
            return render(request,'update.html', {'text':t})
        obj.priority= pri_val
        obj.task=name
        obj.due_date=update_date
        obj.person_id = person_id
        obj.save()
        return HttpResponseRedirect('/')

def new_passwd(request):
    if request.method == 'POST':
        person_id = request.session.get('user_login', None)
        old_password= request.POST.get("old_pass", None)
        new_password = request.POST.get("new_pass", None)
        try:
            new_pass_valid = Registration.objects.get(id = person_id, password= old_password)
            print "new password %s" % new_password
            new_pass_valid.password = new_password
            new_pass_valid.save()
            return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            t = "Old password is invalid"
            return render(request,'change_passwd.html', {'text':t}) 
    return render(request, 'change_passwd.html') 
        




