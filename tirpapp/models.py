from tkinter import CASCADE
from django.db import models
import re
import bcrypt
import datetime



class UserManager(models.Manager):
    def register_validation(self,postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['fname'] = "First Name must be more than 2 characters "

        if len(postData['lname']) < 2:
            errors['lname'] = "Last Name must be more than 2 characters "

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        else:
            try:
                user = User.objects.get(email__iexact=postData['email'])
                errors['email'] = "Email is already registered try to login!"  
            except:
                pass

        if postData['password'] != postData['confirm_password']:
            errors["passwords"] = "passwords are not matched!" 

        if len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters" 
        
        return errors

    def login_validation(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        else:
            try:
                user = User.objects.get(email__iexact=postData['email'])
                if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                    errors['login'] = "Email or Password is incorrect !"
            except:
                errors['login'] = "Email or Password is incorrect !"
        
        return errors

      

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()



class wishManager(models.Manager):
    def wish_validation(self,postData):
        errors = {}
        if len(postData['makewish']) < 2:
            errors['makewish'] = "wish must be more than 3 characters "

        if len(postData['description']) < 5:
           errors['description'] = " description must be more than 2 characters "

        return errors

class Wish(models.Model):
    
    wish=models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,related_name='wihes',on_delete=models.CASCADE)
    objects = wishManager()
    
class grand(models.Model):
    item=models.CharField(max_length=255)
    dateadd=models.DateTimeField(auto_now=True)
    grantedadd=models.DateField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="likes")
    user=models.ForeignKey(User,related_name='granted_wi',on_delete=models.CASCADE)
