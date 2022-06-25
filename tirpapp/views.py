from ast import If
from multiprocessing import context
from django.shortcuts import render, redirect
from flask import request
from tirpapp.models import User
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request,'index.html')


def register(request):



    if request.method == 'POST':
        errors = User.objects.register_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        else:

            hash_pass = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                password=hash_pass
            )
        user.save()
        messages.success(request, "user seccessfully adedd")

        request.session['user_id'] = user.id

        return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            userid = User.objects.get(email__iexact=request.POST['email'])
            request.session['user_id'] = userid.id
        return redirect('/success')

    return redirect('/')

def success(request):

    if 'user_id' not in request.session:
     return redirect('/')

    _user = User.objects.get(id=request.session['user_id'])
    context = {
        'user':_user,
        'your_wish':Wish.objects.filter(user=_user).order_by("created_at"),
        'granted_wishes':grand.objects.all(),
       }
    return render(request,'dashboord.html',context)

def logout(request):
    del request.session['user_id']
    return redirect('/')



def new_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request,'create_wish.html',context)

def create_wish(request):

    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        errors = Wish.objects.wish_validation(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
        
                _user = User.objects.get(id=request.session['user_id'])
                makeiwsh = Wish.objects.create(
                wish = request.POST['makewish'],
                description = request.POST['description'],
                user = _user
                )
            
            makeiwsh.save()
            messages.success(request,"wish added successfully!")
            return redirect('/success')
    return redirect("/wish/new")

def editwish (request, wish_id):
 _wish= Wish.objects.get(id=wish_id)
 context={
    'wish':_wish

 }
 return render (request,'edit_wish.html',context)

def stats(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'granted':grand.objects.all()
    }
    return render(request,'stats.html',context)

def udpdate_wish(request, wish_id):
    if request.method == 'POST':
         _wish= Wish.objects.get(id=wish_id)
         _wish.wish = request.POST['makewish'],
         _wish.description = request.POST['description'],
         _wish.save()
         return redirect ('/success')
    return redirect(f'/wish/{wish_id}/edit')

def wish_destroy(request, wish_id):
    _wish= Wish.objects.get(id=wish_id)
    _wish.delete()

    return redirect('/success')


def grant_wish(request,wish_id):
    _wish = Wish.objects.get(id=wish_id)
    _user = User.objects.get(id=request.session['user_id'])
    gn = grand.objects.create(
        item = _wish.wish,
        user = _user
    )
    gn.save()
    _wish.delete()

    return redirect('/success')


def granted_like(request,granted_id):
    _user = User.objects.get(id=request.session['user_id']) 
    gn = grand.objects.get(id = granted_id)

    gn.like.add(_user)
    gn.save()

    return redirect('/success')



