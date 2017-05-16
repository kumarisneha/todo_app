# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from todoapp.models import Todolist, Registration
from todoapp.utils import hashed_func
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from todo.celery import send_multi_mail, some_task, send_mail_task
import base64
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages

# from django.core.mail import send_mail
# send_mail('Django Mail', 'First message using django.', 'kumarisneha102@gmail.com', ['snehatezu@gmail.com'], fail_silently=False)
# Create your views here.
def registration_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name', None)
        emailid = request.POST.get('email_id', None)
        passwd= request.POST.get('passwd', None)
        confirm_password= request.POST.get('confirm_new_pass', None)
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
                if passwd == confirm_password:
                    a = Registration(user_name = user_name, email_id = emailid, password= hashed_func(passwd))
                    a.save()
                    user_email= a.email_id
                    email_encode= base64.b64encode(user_email)
                    print email_encode
                    subject, from_email, to = 'hello %s' % str(a.user_name), 'snehatezu@gmail.com', user_email
                    text_content = 'Complete registration with to-do app'
                    html_content ='<a href="http://127.0.0.1:8000/verification/%s"> <p>Click here to complete your registration</p></a>' % email_encode
                    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    # msg.attach_alternative(html_content, "text/html")
                    # msg.send()
                    send_multi_mail.delay(subject, text_content,html_content, from_email, to)
                else:
                    compare = "The password you entered do not match"
                    return render(request,'registration.html', {'text':compare})

            except IntegrityError:
                t = "This user already exists"
                return render(request,"registration.html", {'text': t})
            t = "You have succesfully registered and your registration email is sent to your email id" 
            return render(request,'registration.html', {'text':t})
        except ValidationError:
            t = "oops!!! wrong email"
            return render(request,"registration.html", {'text': t})                 
    return render(request, 'registration.html')

def verify(request, code):

    email_decode = base64.b64decode(code)
    print email_decode
    obj=Registration.objects.get( email_id= email_decode )
    obj.email_verified = True
    obj.save()
    return HttpResponseRedirect('/')

def login_page(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id', None)
        passwd= request.POST.get('passwd',None)
        print request.POST
        print email_id
        print passwd
        try:
            email_val= Registration.objects.get(email_id = email_id, password = hashed_func(passwd))
            if email_val.email_verified == True:
                request.session['user_login'] = email_val.id
                return HttpResponseRedirect('/')
            else:
                t = "You have not verified your email" 
                return render(request,'login.html', {'text':t})
        except ObjectDoesNotExist:
            t = "Email or password is not valid. Please try again" 
            return render(request,'login.html', {'text':t})     
    return render(request, 'login.html')

def logout(request):
    try:
        del request.session['user_login']
    except KeyError:
        pass
    return render(request, 'login.html')

def login_valid(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id', None)
        passwd= request.POST.get('passwd',None)
        print email_id
        print passwd
        try:
            email_val= Registration.objects.get(email_id = email_id, password = hashed_func(passwd))
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
            'choose': int(choose),
            }
    else:
        context={
            'todo_list': Todolist.objects.filter(person_id = person_id).order_by('priority'),
            'username': Registration.objects.get(id=person_id).user_name,
            'user': Registration.objects.get(id=person_id).user_name.split(" ")[0],
            'user_id': Registration.objects.get(id=person_id).id,
            'emailid': Registration.objects.get(id=person_id).email_id,
            'choose': int(choose),
            }     
    return render(request, 'index.html', context)

def email_notification(request):
    person_id = request.session.get('user_login', None)
    if request.method == 'POST':
        check_mail = request.POST.get('check_mail', None)
        print "Print somethinmg"
        print check_mail
        if check_mail == None:
            obj = Registration.objects.get(id=person_id)
            obj.email_active = 0
            obj.save()
            print obj.email_active
            return HttpResponseRedirect('/')
        else:
            obj = Registration.objects.get(id=person_id)
            obj.email_active = 1
            obj.save()
            print "here"
            print obj.email_active
            return HttpResponseRedirect('/')
    context={
    'username': Registration.objects.get(id=person_id).user_name,
    'user': Registration.objects.get(id=person_id).user_name.split(" ")[0],
    'emailid': Registration.objects.get(id=person_id).email_id,
    'email_active': Registration.objects.get(id=person_id).email_active,
    }
    return render(request,'email_notification.html',context)

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
    context={
    'username': Registration.objects.get(id=person_id).user_name,
    'user': Registration.objects.get(id=person_id).user_name.split(" ")[0],
    'emailid': Registration.objects.get(id=person_id).email_id,
    'xyz': obj}
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
    person_id = request.session.get('user_login', None)
    if request.method == 'POST':
        person_id = request.session.get('user_login', None)
        old_password= request.POST.get("old_pass", None)
        new_password = request.POST.get("new_pass", None)
        confirm_password = request.POST.get("confirm_new_pass", None)
        try:
            new_pass_valid = Registration.objects.get(id = person_id, password= hashed_func(old_password))
            print "new password %s" % new_password
            if new_password == confirm_password:
                new_pass_valid.password = hashed_func(new_password)
                new_pass_valid.save()
            else:
                compare = "The new password you entered does not match"
                return render(request,'change_passwd.html', {'text':compare})
            return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            tt = "Old password is invalid"
            return render(request,'change_passwd.html', {'text':tt}) 
    context={
    'username': Registration.objects.get(id=person_id).user_name,
    'user': Registration.objects.get(id=person_id).user_name.split(" ")[0],
    'emailid': Registration.objects.get(id=person_id).email_id,
    }
    return render(request, 'change_passwd.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email_id = request.POST.get("send_email", None)
        obj=Registration.objects.get( email_id= email_id)
        print email_id
        email_encode= base64.b64encode(email_id)
        subject, from_email, to = 'Reset your to-do list password', 'snehatezu@gmail.com', email_id
        text_content = 'Complete registration with to-do app'
        html_content ='<a href="http://127.0.0.1:8000/reset_password/%s"> <p>Please click on the link below in order to reset your password.</p></a>' % email_encode
        #msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        #msg.attach_alternative(html_content, "text/html")
        #msg.send()
        send_multi_mail.delay(subject, text_content,html_content, from_email, to)
        messages.info(request, 'We have sent you a link to reset your password!')
        return render(request,'forgot_password.html')
    return render(request, 'forgot_password.html')
    
def forgot_pass_verify(request, code):
    encode_val=code
    email_decode= base64.b64decode(code)
    print email_decode
    print "not working"
    if request.method == 'POST':
        new_passwd = request.POST.get('new_password', None)
        confirm_passwd= request.POST.get('confirm_new_password',None)
        if new_passwd == confirm_passwd:
            obj= Registration.objects.get(email_id = email_decode)
            obj.password = hashed_func(confirm_passwd)
            obj.save()
            print obj.password
            request.session['user_login'] = obj.id
            return HttpResponseRedirect('/')            
        else:
            t = "Password does not match" 
            return render(request,'reset_passwd.html', {'text':t})  
    context = {'email_code': encode_val, }
    return render(request, 'reset_passwd.html',context)
