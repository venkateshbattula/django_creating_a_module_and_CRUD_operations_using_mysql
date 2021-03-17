from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home/', views.home, name='index'),
    path('demo/<int:a>/<int:b>/', views.demo, name='demo'),
    path('formdemo/', views.formdemo, name='formdemo'),
    path('addlocation/', views.addLocation, name='addlocation'),
    path('showlocations/', views.showlocations, name='showlocations'),
    path('updatelocation/<int:id>', views.updateLocation, name='updatelocation'),
    path('deletelocation/<int:id>', views.deletelocation, name='deletelocation'),
    path('addemployee/', views.addemployee, name='addemployee'),
    path('showemployees/', views.showemployees, name='showemployees'),
    path('updateemployee/<int:id>', views.updateemployee, name='updateemployee'),
    path('deleteemployee/<int:id>', views.deleteemployee, name='deleteemployee'),
    path('registartion/', views.register, name='registartion'),
]
