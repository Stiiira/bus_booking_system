import time, datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.

shuttle_unit = 3
seats_per_bus = 40

def initView(request):
	bus_drivers = [{'username':'driver1', 'password':'1234', 'email':'driver@123.com', 'bus':'bus1'},
				   {'username':'driver2', 'password':'1234', 'email':'driver@123.com', 'bus':'bus2'},
				   {'username':'driver3', 'password':'1234', 'email':'driver@123.com', 'bus':'bus3'}]
	manager = {'username':'manager', 'password':'1234', 'email':'manager@123.com'}
	routes = ['route1', 'route2', 'route3']
	stations = [['station_1_1', 'station_1_2', 'station_1_3', 'station_1_4'],
				['station_2_1', 'station_2_2', 'station_2_3', 'station_2_4'],
				['station_3_1', 'station_3_2', 'station_3_3', 'station_3_4']]
	driver_ids = []
	for d in bus_drivers:
		bus = Bus(bus_name=d['bus'])
		bus.save()
		try:
			driver = Bus_driver.objects.create_user(d['username'], d['email'], d['password'], bus=bus)
			driver_ids.append(driver.id)
			driver.save()
		except Exception as e:
			print(e)
			driver_ids.append(Bus_driver.objects.get(username=d['username']).id)
		# bus.save()
	try:
		ma = Employee.objects.create_user(manager['username'], manager['email'], manager['password'])
	except Exception as e:
		print(e)
	for i, r in enumerate(routes):
		try:
			Route.objects.get(Route_name=r)
			continue
		except Exception as e:
			print(e)
		route = Route(Route_name = r)
		route.save()
		station = stations[i]
		for j, s in enumerate(station):
			sta = Station(station_name=s, price=j+1, route_id=route)
			sta.save()
		for i in range(shuttle_unit):
			for di in ['TO', 'FROM']:
				shuttle = Shuttle(route_id=route,
					direction=di, departure_time=datetime.time(8+i*4,0,0),
					driver_id=Bus_driver.objects.get(id=driver_ids[i]))
				shuttle.save()
	try:
		user = Customer.objects.get(username='haha')
	except Exception as e:
		print(e)
		user = Customer.objects.create_user('haha','','1234')
		user.save()
	return HttpResponse('Successfully create data.')


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
			return redirect('driver_search')
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
			return redirect('manager_inspect')
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
		route_ids.append({'id':route_id, 'name':r.Route_name})
	return render(request, 'busbooking/userbuy.html',
			{'route_ids': route_ids})

@login_required
def userBuyRequest(request):
	route_id = int(request.POST['route_id'])
	direction = int(request.POST['direction'])
	return redirect('user_buy_time', line=route_id, direction=direction)

@login_required
def userBuyTime(request, line, direction):
	direction_str = 'TO'
	if direction == 2:
		direction_str = 'FROM'
	shuttles = Shuttle.objects.filter(route_id=line, direction=direction_str).order_by('shuttle_id')
	shuttle_list = []
	for s in shuttles:
		orders = Order.objects.filter(shuttle_id=s.shuttle_id)
		sold_num = 0
		for o in orders:
			sold_num = sold_num + o.number
		shuttle_list.append({
			'time': '{}:{}'.format(str(s.departure_time.hour).zfill(2), str(s.departure_time.minute).zfill(2)),
			'id': s.shuttle_id,
			'number': seats_per_bus - sold_num
		})
	station_list = []
	stations = Station.objects.filter(route_id=line).order_by('station_id')
	for s in stations:
		station_list.append({
			'name': s.station_name,
			'id': s.station_id
		})
	return render(request, 'busbooking/userbuytime.html',
			{'shuttle_list': shuttle_list, 'station_list': station_list, 'numbers': range(1,4)})

@login_required
def userBuyRequestTime(request):
	shuttle_id = int(request.POST['shuttle_id'])
	station_id = int(request.POST['station_id'])
	orders = Order.objects.filter(shuttle_id=shuttle_id)
	sold_num = 0
	for o in orders:
		sold_num = sold_num + o.number
	number = int(request.POST['number'])
	if sold_num + number > 40:
		return redirect('user_buy')
	customer_id = request.user.id
	fee = get_object_or_404(Station, station_id=station_id).price
	try:
		order = Order()
		order.shuttle_id = get_object_or_404(Shuttle,shuttle_id=shuttle_id)
		order.station_id = get_object_or_404(Station, station_id=station_id)
		order.number = number
		order.customer_id = get_object_or_404(Customer, id=customer_id)
		order.ispayment = True
		order.paymentamount = fee*number
		order.save()
		for i in range(number):
			ticket = Ticket(order_id=order, seat_id=sold_num+i+1, validate=False)
			ticket.save()
	except Exception as e:
		print(e)
		return redirect('user_buy')
	return redirect('user_success')

@login_required
def userSuccess(request):
	return render(request, 'busbooking/success.html')

@login_required
def userLookup(request):
	user_id = request.user.id
	orders = Order.objects.filter(customer_id=get_object_or_404(Customer, id=user_id)).order_by('-order_id')
	order_list = []
	for o in orders:
		time = o.shuttle_id.departure_time
		time_str = '{}:{}'.format(str(time.hour).zfill(2), str(time.minute).zfill(2))
		for ticket in Ticket.objects.filter(order_id=o).order_by('-ticket_id'):
			order_list.append({
				'id': o.order_id,
				'shuttle': o.shuttle_id.shuttle_id,
				'line': o.shuttle_id.route_id.Route_name,
				'station': o.station_id.station_name,
				'time': time_str,
				'direction': o.shuttle_id.direction,
				'price': int(o.paymentamount/o.number),
				'ticket_id': ticket.ticket_id,
				'seat': ticket.seat_id,
				'validation': str(ticket.validate),
			})
	return render(request, 'busbooking/userlookup.html', {'order_list': order_list})


@login_required
def driversearch(request):
	username = request.user.username
	# shuttles = Shuttle.objects.filter(driver_id=username).order_by('shuttle_id')
	shuttles = Shuttle.objects.filter().order_by('shuttle_id')
	shuttle_list = []
	for s in shuttles:
		shuttle_list.append({
			'shuttle_id': s.shuttle_id,
		})
	return render(request, 'busbooking/driversearch.html', {'username': username,'shuttle_list': shuttle_list})



@login_required
def driversearchRequest(request):
	shuttle = int(request.POST['shuttle_id'])
	return redirect('driver_validate', shuttle=shuttle)


@login_required
def drivervalidate(request,shuttle):
	# return redirect('user_buy_time', shuttle=shuttle)
	return render(request, 'busbooking/drivervalidate.html')


@login_required
def drivervalidateRequest(request):
	return redirect('driver_validate')


@login_required
def managerinspect(request):
	pass
	orders = Order.objects.filter().order_by('-order_id')
	order_list = []
	for o in orders:
		time = o.shuttle_id.departure_time
		time_str = '{}:{}'.format(str(time.hour).zfill(2), str(time.minute).zfill(2))
		for ticket in Ticket.objects.filter(order_id=o).order_by('-ticket_id'):
			order_list.append({
				'id': o.order_id,
				'customer':o.customer_id.username,
				'shuttle': o.shuttle_id.shuttle_id,
				'line': o.shuttle_id.route_id.Route_name,
				'station': o.station_id.station_name,
				'time': time_str,
				'direction': o.shuttle_id.direction,
				'ticket_id': ticket.ticket_id,
				'seat': ticket.seat_id,
				'ispayment': o.ispayment,
				'validation': str(ticket.validate),
			})
	return render(request, 'busbooking/managerinspect.html', {'order_list': order_list})
