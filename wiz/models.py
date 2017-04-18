from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lab(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    description = models.TextField(max_length=500, blank=True)
    t_begin = models.DateTimeField()
    t_end = models.DateTimeField()
    address = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return str(self.teacher)+'@'+str(self.name)+'@'+str(self.t_begin)
