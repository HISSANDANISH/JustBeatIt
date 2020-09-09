from django.urls import path
from django.conf.urls import include
from accounts import views 
urlpatterns = [
    path('register',views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]