
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
import mysql.connector



urlpatterns = [
    path('', views.home, name='home'),
    path('aboutme/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path('route/', views.route, name='route'),
]

