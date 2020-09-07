from django.urls import path
from django.conf.urls import include
from music import views as v
urlpatterns = [
    path('',v.index, name='index'),
]