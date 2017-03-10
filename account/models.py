from django.db import models

# Create your models here.
from django.contrib.auth.models import User
#from .fields import AutoOneToOneField

#class Work(models.Model):
#    work = models.CharField(max_length = 100, verbose_name = 'Работа')

#class Profile(models.Model):
#    user = AutoOneToOneField(User, related_name='profile', verbose_name=('User'), primary_key=True)
#    work = models.ForeignKey(Work, verbose_name = 'Вид деятельности')
