import json
from django.shortcuts import render, redirect
from django.http import Http404
from .models import UserProfile, Hobby, User
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from django.core.mail import EmailMessage
from django.core import serializers
from django.views.generic import CreateView
import datetime as dt


class UserProfileCreateView(CreateView):
    model = UserProfile
    fields = ('username','name', 'email', 'dateOfBirth', 'hobbies','gender', 'password1', 'password2')
appname = "PhoenixFortune"

# decorator
def loggedin(view):
    def mod_view(request):
        if 'username' in request.session:
            username = request.session['username']
            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                raise Http404('UserProfile does not exist')
            return view(request, user)
        else:
            return render(request, 'socialApp/errorLogin.html', {})

    return mod_view

 # view for index/, shows to the user the index page where they can select to register or login
def index(request):
    context = {'appname': appname}
    return render(request, 'socialApp/index.html', context)


def signup(request):
    context = {'appname': appname}
    return render(request, 'socialApp/signup.html', context)


def hobbies(request):
    total = Hobby.objects.all()  # Querydict all the hobbies
    qdict = {
        'hobby': total
    }
    return render(request, "socialApp/signup.html", context=qdict)

 # register view, is called by the signup page and registers the user with the information entered on the html form
def register(request):
    condition = register
    if  request.method =='POST':# Check if the request was POST
        dict = validate(request, condition) # validate if data is all nice and clean and ready to go
        #dict{username, name, email, hobbies, dataofBirth, gender, image, }
        user = UserProfile(username=dict[0], name=dict[1], email=dict[2], dateOfBirth=dict[4], gender=dict[5],image=dict[6])
        try:
            user.set_password(dict[7]) ##UserProfile also inherits User so takes the password aspect
            user.save()
            for hobby in dict[3]:  #iterate through m2m hobby field
                hobgob, x = Hobby.objects.get_or_create(name=hobby) #Will only fail if there is a duplicate Hobby existing that is identical so testing to see
                user.hobbies.add(hobgob)
        except IntegrityError:
            raise Http404("Username isn't unique! Please choose another one!")
        email = EmailMessage('Yo,'+ dict[0] + '. thanks for coming along and playing!', to=[dict[2]])
        #email.send()
        context = {
            'appname': "hobby",
            'username': dict[0]
        }
        return render(request, 'socialApp/successful.html', context)



def login(request):#is used to login the user
    if not request.method == 'POST':
        context = {'appname': appname}
        return render(request, 'socialApp/login.html', context)
    else:
        username = request.POST['username']
        password = request.POST['password']
        try:
            userProfile = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            raise Http404('User does not exist')
        if userProfile.check_password(password):

            request.session['username'] = username
            request.session['password'] = password
            context = {
                'appname': appname,
                'username': username,
                'loggedin': True
            }
            response = render(request, 'socialApp/login.html', context)
            ## cookie most code from lab8
            now = dt.datetime.utcnow()
            max_age = 365 * 24 * 60 * 60  # one year
            delta = now + dt.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = dt.datetime.strftime(delta, format)
            response.set_cookie('last_login', now, expires=expires)
            return response
        else:
            raise Http404('Wrong password')


@loggedin#decorator that verifies the user is logged in. if he is, the following view can be called
def logout(request, user):  # view for logout/, flushes the session and logs out the user
    request.session.flush()
    context = {'appname': appname}
    return render(request, 'socialApp/logout.html', context)

# validate all the fields passed in the request
def validate(request, condition):
    u = request.POST['uname']
    f = request.POST['fname']
    e = request.POST['email']
    g = request.POST['gender']
    h = request.POST.getlist('hobby')
    d = request.POST['dob']
    i = request.FILES.get('img_file',False)
    dict = [u, f, e, h, d, g, i]  # creates an array containing all the fields
    if condition == register:
        p = request.POST['password']
        dict.append(p)
    return dict

@loggedin
def logout(request, user):
    request.session.flush()
    context = { 'appname': appname }
    return render(request,'socialApp/logout.html', context)

@loggedin
def profile(request, user):#view that will allow the user to edit his profile
    user1 = UserProfile.objects.filter(username=user)  # QuerySet object
    condition = profile
    if request.POST:
        dict = validate(request, condition)
        user1.update(first_name=dict[1], email=dict[2], dob=dict[4])  # updates the fullname and email
        user.hobbies.clear()  # clears hobby
        for hobby in dict[3]:  # dict[4] is the list of hobbies
            hob, _ = Hobby.objects.get_or_create(name=hobby)
            user.hobbies.add(hob)
    total = Hobby.objects.all()  # Queryset, all the hobbies
    dict = {
        'appname': appname,
        'email': user1[0].email,
        'password': user1[0].password,
        'username': user1[0].username,
        'name': user1[0].name,
        'loggedin': True,
        'age': calculate_age(user1[0].dateOfBirth),
        'hobby': total,
        'image': user1[0].image,
        'gender': user1[0].gender,
        'dob': user1[0].dateOfBirth
    }
    return render(request, 'socialApp/profile.html', context=dict)

@loggedin
def homepage(request, user):# view of the homepage.
    members = UserProfile.objects.all()
    members = excludematched(members, user)#excludes matched users from the list of users that will be presented to the logged in user
    sort = sorting(members, user)#sorts the remaining list of users and saves it in sort.
    context = {
        "members": sort, #passes the sorted list of users in the context
        "loggedin":True
    }
    return render(request, 'socialApp/homepage.html', context)#renders the sorted list of users that the logged in user is not matched with.

def calculate_age(dob): #view that returns the age from the dob of the user.
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
