from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Hobby(models.Model): #Hobby model to be used in a m2m relationship
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class UserProfile(User): #Inherit from User
	image = models.ImageField(upload_to='profile_images')
	GENDERS = (
			('Male', 'Male'),
			('Female', 'Female'),
		)
	gender = models.CharField(max_length=6,choices=GENDERS)  #Gender field
	dateOfBirth = models.DateField() #Date Of Birth
	name = models.CharField(max_length=130)
	hobbies = models.ManyToManyField(
        to=Hobby,
        symmetrical=False,
        blank=False
    )
	favourites = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False
    )

	def __str__(self):
		return self.username
