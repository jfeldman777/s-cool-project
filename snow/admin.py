from django.contrib import admin

# Register your models here.
from .models import UserProfile as Profile
from .models import ExpertStatus
from .models import TutorStatus, ExamRecord

from .models import Course
from .models import Lecture
from .models import Question

admin.site.register(Profile)
admin.site.register(ExpertStatus)
admin.site.register(TutorStatus)

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(ExamRecord)
