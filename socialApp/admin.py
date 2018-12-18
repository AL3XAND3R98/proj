from django.contrib import admin

from .models import UserProfile, Hobby

class UserProfileAdmin(admin.ModelAdmin):
    fields = ('username','email','password','image','name', 'gender','dob','hobbies')


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Hobby)
