from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import json
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items(): 
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/dashboard')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/dashboard')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context)

def post_message(request):
    Wall_Message.objects.create(
        message = request.POST['message'],
        poster = User.objects.get(id=request.session['user_id']))
    return redirect('/success')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(
        comment=request.POST['comment'],
        poster=poster,
        wall_message=message)
    return redirect('/success')

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

# def delete_post(request, id):
#     erase = Wall_Message.objects.get(id=id)
#     erase.delete()
#     return redirect('/success')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect("/")
    user = User.objects.get(id = request.session['user_id'])
    context = {
		"user": user,
		"user_trips":Trip.objects.filter(creator = user),
        "joined_trips" : Trip.objects.filter(joined=user),
		"other_trips": Trip.objects.all().exclude(creator=user).exclude(joined=user),
	}
    return render(request,"trips.html",context)

def new(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request,"newtrip.html",context)

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')

def create(request):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/trips/new")
        Trip.objects.create(
            destination =request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan=request.POST['plan'],
            creator=User.objects.get(id=request.session['user_id'])
        )
    return redirect("/dashboard")

def show(request, id):
    quotes = "https://zenquotes.io/api/random"
    response = requests.get(quotes).json()
    context={
        'trip':Trip.objects.get(id=id),
        'quotes': response[0]
    }
    return render(request,"display.html",context)

def edit(request, id):
    context={
        'trip':Trip.objects.get(id=id)
    }
    return render(request,"edit.html",context)

def update(request, id):
    if request.method == "POST":
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/trips/edit/{id}")
        else:
            trip=Trip.objects.get(id=id)
            trip.destination=request.POST['destination']
            trip.start_date=request.POST['start_date']
            trip.end_date=request.POST['end_date']
            trip.plan=request.POST['plan']
            trip.save()
    return redirect('/dashboard')

def join(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    user.joined_trips.add(trip)
    return redirect("/dashboard")

def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect("/dashboard")

def cancel(request, id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    user.joined_trips.remove(trip)
    return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect('/')