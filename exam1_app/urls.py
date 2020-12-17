from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
############################################
    path('wishes/new', views.add_form),
    path('make_wish', views.make_wish),
    path('edit_form/edit/<int:num>', views.edit_form),
    path('wishes/edit/<int:num>', views.edit_wish),
    path('remove/<int:num>', views.remove),
    path('grant_wish/<int:num>', views.grant_wish),
    path('like_wish/<int:num>', views.like_wish),
    path('unlike_wish/<int:num>', views.unlike_wish),
    path('wishes/stats', views.wishes_stats),
    
    
]
