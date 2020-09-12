from django.urls import path
from django.conf.urls import include
from accounts import views 
urlpatterns = [
    path('register',views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name= 'home'),
    path('friend_list',views.friend_list, name='friend_list'),
    path('users_list',views.users_list, name='users_list'),
    path('send_friend_request', views.send_friend_request, name='sfr'),
    path('cancel_friend_request', views.cancel_friend_request, name='sfr')
]