from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StudentTutorContract(models.Model):
    student = models.ForeignKey(User, \
        on_delete=models.CASCADE, related_name = "student_seeks_tutor")
    tutor = models.ForeignKey(User, \
        on_delete=models.CASCADE, related_name = "tutor_seeks_student")
    student_yes = models.BooleanField(default=True)
    tutor_yes = models.BooleanField(default=False)
    distant_yes = models.BooleanField(default=False)

    def __str__(self):
        return self.tutor.get_full_name() + '@'  + self.student.get_full_name()
