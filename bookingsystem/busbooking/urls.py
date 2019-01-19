from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('loginredirect/', views.loginRedirect, name='login_redirect'),
	path('userlogin/', views.userLogin, name='user_login'),
	path('userloginrequest/', views.userLoginRequest, name='user_login_request'),
	path('driverlogin/', views.driverLogin, name='driver_login'),
	path('managerlogin/', views.managerLogin, name='manager_login'),
	path('signup/', views.signup, name='user_signup'),
]
