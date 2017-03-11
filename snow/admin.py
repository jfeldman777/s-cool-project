from django.contrib import admin

# Register your models here.
from .models import UserProfile as Profile

admin.site.register(Profile)
