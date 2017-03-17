from django.db import models
from django.contrib.auth.models import User
from smartfields import fields

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    #picture = models.ImageField(null=True);
    picture = fields.ImageField(null=True);

    site = models.URLField(null=True)

    def __str__(self):
        return self.user.username


    #website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to='profile_images', blank=True)
    #фото



    #is_student = models.BooleanField(blank=False)
    #is_tutor = models.BooleanField(blank=False)
    #is_expert = models.BooleanField(blank=False)
    #is_tech = models.BooleanField(blank=False)
    #is_god = models.BooleanField(blank=False)
    '''

class InboxMessage(models.Model):
    subject = models.CharField(max_length=80)
    body = models.CharField(max_length=250)
    userfrom = models.ForeignKey(User)
    userto = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    isopen = models.BooleanField(default = False)

    def __str__(self):
        return str(self.id)+':'+userfrom+'>>'+userto+':'+subject[:10]
'''
