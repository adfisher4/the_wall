from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if len(postData['first_name']) < 1:
            errors['first_name'] = 'First name field must be filled'
        if len(postData['last_name']) < 1:
            errors['last_name'] = 'Last name field must be filled' 
        try:
            User.objects.get(email=postData['email'])
            errors['email'] = 'email is already registered... go ahead and login!'
        except:
            pass
        if len(postData['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters'
        if (postData['password']) != (postData['confirm_pw']):
            errors['password'] = 'Passwords must be the same'
        if not EMAIL_REGEX.match(postData['email']):
            print("reached")
            errors['email'] = 'Not a valid email'
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    key = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    key = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, related_name='comments')
    post_to = models.ForeignKey(Message, related_name='comments_received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



