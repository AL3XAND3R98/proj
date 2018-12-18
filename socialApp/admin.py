from django.contrib import admin

from .models import UserProfile, Hobby

admin.site.register(UserProfile)
admin.site.register(Hobby)
