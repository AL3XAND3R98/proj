"""webProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    # welcome page
    path('', views.index, name='index'),
    # signup page
    path('signup/', views.hobbies, name='signup'),
    # register new user
    path('register/', views.register, name='register'),
    # login page
    path('login/', views.login, name='login'),
    # logout page
    path('logout/', views.logout, name='logout'),
    # selects the current hobbies
    #path('hobby/', views.hobby, name='hobby'),
    # user profile edit page
    path('profile/', views.profile, name='profile'),
    # the user matches page
    #path('mymatches/', views.mymatches, name='mymatches'),
    # search with all the available matches
    path('homepage/', views.homepage, name='search'),

    # Ajax: match with a member
    #path('homepage/match/', views.match, name='match'),
    # Ajax: upload image
    #path('profile/uploadimage/', views.upload_image, name='uploadimage'),
    # Ajax: filter available matches
    #path('search/filtered/', views.filter, name='filteredage'),
    # Ajax: unmatch with a member
    #path('mymatches/unmatch/', views.unmatch, name='unmatch'),

    # members page
    #path('homepage/<str:username>/', views.users_profile, name='users_profile'),
    #path('mymatches/<str:username>/', views.users_profile, name='users_profile'),
]

# TODO
