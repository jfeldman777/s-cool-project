from django.contrib import admin

# Register your models here.
from .models import UserProfile as Profile
from .models import ExpertStatus
from .models import TutorStatus

admin.site.register(Profile)
admin.site.register(ExpertStatus)
admin.site.register(TutorStatus)
