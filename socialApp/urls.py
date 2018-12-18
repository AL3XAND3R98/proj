
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.hobbies, name='signup'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('hobby/', views.hobby, name='hobby'),
    path('profile/', views.profile, name='profile'),
    path('homepage/', views.homepage, name='homepage'),
    path('search/', views.homepage, name='search'),
]

# TODO
