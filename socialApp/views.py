import json
from django.shortcuts import render, redirect
from django.http import Http404
from .models import UserProfile, Hobby, User
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.core import serializers
import datetime as dt

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

    return render(request, 'socialApp/index.html',)



def hobbies(request):
    total = Hobby.objects.all()  # Querydict all the hobbies
    qdict = {
        'hobby': total
    }
    print(total)
    return render(request, "socialApp/register.html", context=qdict)

 # register view, is called by the signup page and registers the user with the information entered on the html form
def register(request):
    total = Hobby.objects.all()
    if  request.method =='POST':# Check if the request was POST
        dict = validate(request) # validate if data is all nice and clean and ready to go
        #dict{username, name, email, hobbies, dataofBirth, gender, image, }
        user = UserProfile(username=dict[0], name=dict[1], email=dict[2], dob=dict[4], gender=dict[5],image=dict[6])
        try:
            user.set_password(dict[7]) ##UserProfile also inherits User so takes the password aspect
            user.save()
            for hobby in dict[3]:  #iterate through m2m hobby field
                hobgob, x = Hobby.objects.get_or_create(name=hobby) #Will only fail if there is a duplicate Hobby existing that is identical so testing to see
                user.hobbies.add(hobgob)
        except IntegrityError:
            return render(request, 'socialApp/register.html', {
                'error_message': "Username " + request.POST['username'] + " already exists!",
                'hobby': total
            })
        context = {
            'registration': True,
            'hobby': total
        }
        return render(request, 'socialApp/login.html', context)
    return render(request, 'socialApp/register.html')

def login(request):
    if not ('username' in request.POST and 'password' in request.POST):
        return render(request,'socialApp/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        try:
            userProfile = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return render(request,'socialApp/login.html',{
             'error_message2': "Username Doesn't exist"
             })
        if userProfile.check_password(password):

            request.session['username'] = username
            request.session['password'] = password
            context = {
                'username': username,
                'loggedin': True
            }
            response = render(request, 'socialApp/homepage.html', context)
            ## cookie most code from lab8
            now = dt.datetime.utcnow()
            max_age = 365 * 24 * 60 * 60  # one year
            delta = now + dt.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = dt.datetime.strftime(delta, format)
            response.set_cookie('login', now, expires=expires)
            #set a cookie
            return response
            print("testoing")
        else:
            return render(request,'socialApp/login.html',{
             'error_message': "Incorrect password, please try again."
             })


@loggedin#decorator that verifies the user is logged in. if he is, the following view can be called
def logout(request, user):  # view for logout/, flushes the session and logs out the user
    request.session.flush()
    return render(request, 'socialApp/index.html')

# validate all the fields passed in the request
def validate(request):
    u = request.POST['username']
    f = request.POST['name']
    e = request.POST['email']
    g = request.POST['gender']
    h = request.POST.getlist('hobby')
    d = request.POST['dob']
    i = request.FILES.get('image')
    p = request.POST['password']
    dict = [u, f, e, h, d, g, i, p]  # creates an array containing all the fields

    return dict

@loggedin
def logout(request, user):
    request.session.flush()
    return render(request, 'socialApp/logout.html', {
        'logout': "Thanks for logging in! Hope to see you soon :)"
    })

@loggedin
def profile(request, user):#view that will allow the user to edit his profile
    user1 = UserProfile.objects.filter(username=user)  # QuerySet object
    print(user1)
    if request.POST:
        dict = validate(request)
        print(dict)
        user1.update(name=dict[1], email=dict[2], dob=dict[4], gender=dict[5])  # updates the name and

        for hobby in dict[3]:  # dict[4] is the list of hobbies
            hob, _ = Hobby.objects.get_or_create(name=hobby)
            user.hobbies.add(hob)
        user.hobbies.clear()  # clears hobby
    total = Hobby.objects.all()  # Queryset, all the hobbies
    names = user1[0].hobbies.values_list('name', flat=True)
    names = list(names) ## get all hobies in list format
    if(request.FILES.get('image')):
        user.image = request.FILES['image']
    dict = {
        'loggedin': True,
        'email': user1[0].email,
        'password': user1[0].password,
        'username': user1[0].username,
        'name': user1[0].name,
        'age': user1[0].getAge(),
        'hobby': total,
        'image': user1[0].image,
        'gender': user1[0].gender,
        'dob': user1[0].dob,
        'userhobbies': user1[0].hobbies.all(),
        'ownuserhobbies': names,
    }
    return render(request, 'socialApp/profile.html', context=dict)

@loggedin
def homepage(request, user):# view of the homepage.
    members = UserProfile.objects.all()
    #members = excludematched(members, user)#excludes matched users from the list of users that will be presented to the logged in user
    #sort = sorting(members, user)#sorts the remaining list of users and saves it in sort.
    context = {
        "members": "sort", #passes the sorted list of users in the context
        "loggedin":True
    }
    return render(request, 'socialApp/homepage.html', context)#renders the sorted list of users that the logged in user is not matched with.

@loggedin
def hobby(request, user):
    hobby = user.hobbies.all()
    context = serializers.serialize('json', hobby)
    return JsonResponse(context, safe=False)
