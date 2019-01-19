from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.

shuttle_unit = 3

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
	if Customer.objects.filter(username=username):
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('user_index')
	return redirect('user_login')

def driverLogin(request):
	return render(request, 'busbooking/driverlogin.html')

def driverLoginRequest(request):
	username = request.POST['username']
	password = request.POST['password']
	if Bus_driver.objects.filter(username=username):
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
	return redirect('driver_login')

def managerLogin(request):
	return render(request, 'busbooking/managerlogin.html')

def managerLoginRequest(request):
	username = request.POST['username']
	password = request.POST['password']
	if Employee.objects.filter(username=username):
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
	return redirect('manager_login')

def signup(request):
	return render(request, 'busbooking/signup.html')

def signupRequest(request):
	username = request.POST['username']
	password = request.POST['password']
	password_again = request.POST['password_again']
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	if password != password_again:
		return redirect('user_signup')
	if Employee.objects.filter(username=username) or Bus_driver.objects.filter(username=username) or Customer.objects.filter(username=username):
		return redirect('user_signup')
	try:
		user = Customer.objects.create_user(username, '', password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
	except Exception as e:
		print(e)
		return redirect('user_signup')
	return redirect('user_login')

@login_required
def logout_view(request):
	logout(request)
	return redirect('login_redirect')

@login_required
def userIndex(request):
	username = request.user.username
	return render(request, 'busbooking/userindex.html', {'username': username})

@login_required
def userBuy(request):
	routes = Route.objects.order_by('Route_id')
	route_ids = []
	for r in routes:
		route_id = r.Route_id
		route_ids.append(route_id)
	return render(request, 'busbooking/userbuy.html',
			{'route_ids': route_ids})

@login_required
def userBuyRequest(request):
	route_id = int(request.POST['route_id'])
	direction = int(request.POST['direction'])
	shuttles = []
	query_shuttles = Shuttle.objects.filter(route_id=route_id, direction=direction==1?'TO':'FROM').order_by('shuttle_id')
	for s in query_shuttles:
		shuttles.append({
			'time':
		})

@login_required
def userBuyTime(request, line, direction):


@login_required
def userLookup(request):
	return render(request, 'busbooking/userlookup.html')
