from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('loginredirect/', views.loginRedirect, name='login_redirect'),
	path('userlogin/', views.userLogin, name='user_login'),
	path('userloginrequest/', views.userLoginRequest, name='user_login_request'),
	path('driverlogin/', views.driverLogin, name='driver_login'),
	path('driverloginrequest/', views.driverLoginRequest, name='driver_login_request'),
	path('managerlogin/', views.managerLogin, name='manager_login'),
	path('managerloginrequest/', views.managerLoginRequest, name='manager_login_request'),
	path('signup/', views.signup, name='user_signup'),
	path('signuprequest/', views.signupRequest, name='signup_request'),
	path('logout/', views.logout_view, name='logout_request'),
	
	path('userindex/', views.userIndex, name='user_index'),
	path('userbuy/', views.userBuy, name='user_buy'),
	path('userbuyrequest/', views.userBuyRequest, name='user_buy_request'),
	path('userbuytime/', views.userBuyTime, name='user_buy_time'),
	path('userbuyrequesttime/<int:line>/<int:direction>', views.userBuyRequestTime, name='user_buy_request_time'),
	path('userlookup/', views.userLookup, name='user_lookup'),
]
