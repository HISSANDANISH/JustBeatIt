from django.urls import path
from django.conf.urls import include
from accounts import views 
urlpatterns = [
    path('register',views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name= 'home'),
    path('friend_list',views.friend_list, name='friend_list'),
    path('request_list',views.request_list, name='request_list'),
    path('users_list',views.users_list, name='users_list'),
    path('search_users', views.search_users, name='search_users'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('edit_music', views.edit_music, name='edit_music'),
    path('<slug>', views.profile_view, name='profile_view'),
    path('friend_request/send/<int:id>', views.send_friend_request, name='send_friend_request'),
    path('friend_request/accept/<int:id>', views.accept_friend_request, name='accept_friend_request'),
    path('friend_request/cancel/<int:id>', views.cancel_friend_request, name='cancel_friend_request'),
    path('delete_friend/<int:id>', views.delete_friend, name='delete_friend'),
]