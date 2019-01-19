from django.urls import path
from . import views

urlpatterns = [
	path('', view.index, name='index'),
	path('loginredirect/', view.loginRedirect, name='login redirect'),
	path('userlogin/', view.userLogin, name='user login'),
	path('driverlogin/', view.driverLogin, name='driver login'),
	path('managerlogin/', view.managerLogin, name='manager login')
	path('signup/', view.signup, name='user signup'),
]
