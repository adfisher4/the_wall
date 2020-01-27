from django.shortcuts import render, HttpResponse, redirect
from .models import User, Message, Comment 
from django.contrib import messages
from django.contrib.auth import logout
import re
import bcrypt
import datetime



def wall(request):
    context = {
        'all_messages': Message.objects.all().order_by('-created_at'),
        'all_comments': Comment.objects.all(),
        'other_users': User.objects.exclude(email=request.session['email']),
        'user_messages': User.objects.get(email=request.session['email'])
    }
    return render(request, 'wall.html', context)

def index(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/', errors)
        else:
            hash1 = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            print(hash1)
            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1)
            request.session['first_name'] = request.POST['first_name']
            request.session['email'] = request.POST['email']
            return redirect('/wall')

def message(request):
    if request.method == 'POST':
        if len(request.POST['message']) < 2:
            return redirect('/wall')
        else:
            Message.objects.create(key=request.POST['message'], creator=User.objects.get(email=request.session['email']))
            print("Hi Dad")
            return redirect('/wall')

def delete_message(request, id):
    user = User.objects.get(email=request.session['email'])
    message_to_delete = Message.objects.get(id=id)
    
    if request.method == 'POST' and message_to_delete.creator == user and Message.objects.filter(created_at__minute__lte=30):
        comments_to_delete = Comment.objects.filter(post_to=message_to_delete)
        message_to_delete.delete()
        comments_to_delete.delete()

        return redirect('/wall')



def comment(request, id):
    if request.method == 'POST':
        if len(request.POST['comment']) < 2:
            return redirect('/wall')
        else:
            Comment.objects.create(key=request.POST['comment'], creator=User.objects.get(email=request.session['email']), post_to=Message.objects.get(id=id))
            return redirect('/wall')

def login(request):
    errors = {}
    if request.method == 'POST':
        email = request.POST['login_email']
        password = request.POST['login_password']
        try:
            User.objects.get(email=email)
            user = User.objects.get(email=email)
        except:
            errors['email'] = 'email is not registered.'
            for key,value in errors.items():
                messages.error(request, value)
                return redirect('/', errors)
        
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['email'] = email
            request.session['first_name'] = user.first_name
            return redirect('/wall')
        else:
            errors['password'] = 'Password is incorrect'
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/', errors)

def logout_view(request):
    if request.method == 'POST': 
        logout(request)
    return redirect('/')