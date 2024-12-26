from django.contrib import admin
from .models import CustomUser, Hobby

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Hobby)