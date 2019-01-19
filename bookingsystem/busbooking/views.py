from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import *
# Create your views here.

@login_required
def index(request):
	username = request.user.username
	return render(request, 'busbooking/index.html',{'username': username})

def loginRedirect(request):
	return render(request, 'busbooking/loginredirect.html')

def userLogin(request):
	return render(request, 'busbooking/userlogin.html')

def userLoginRequest(request):
	username = request.POST['username']
	password = request.POST['password']
	print(username, password, Customer.objects.get(username=username))
	if Customer.objects.get(username=username):
		user = authenticate(request, username=username, password=password)
		print('user', user)
		if user is not None:
			login(request, user)
			return redirect('index')
	return redirect('user_login')

def driverLogin(request):
	return render(request, 'busbooking/driverLogin.html')

def managerLogin(request):
	return render(request, 'busbooking/managerLogin.html')

def signup(request):
	pass

