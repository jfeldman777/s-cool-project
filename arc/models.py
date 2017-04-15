from django.db import models
from snow.models import Course

class Cat(models.Model):
    name = models.CharField(max_length=50, unique=True)
    books = models.ManyToManyField(Course)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    siblings = models.ManyToManyField('self')

    def __str__(self):
        return self.name
