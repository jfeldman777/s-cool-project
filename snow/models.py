from django.db import models
from django.contrib.auth.models import User
from smartfields import fields

class UserStatus():
    choices = (
        ('E','Empty'),
        ('A','Asked'),
        ('G','Granted'),
        ('D','Delayed'),
        ('B','Blocked'),
    )

    roles = (
        ('S','Student'),
        ('E','Expert'),
        ('T','Tutor')
    )

    def __str__(self):
            return 'EAGDB'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    picture = fields.ImageField(null=True);
    site = models.URLField(null=True, blank=True)

    last_status = models.CharField(max_length=1,
                choices=UserStatus.roles,
                default='S')

    def get_status(self):
        d = dict(UserStatus.roles)
        name = d[self.last_status]
        return name

    def __str__(self):
        return self.user.username


class ExpertStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    EMPTY = 'E'
    status = models.CharField(max_length=1,
            choices=UserStatus.choices,
            default=EMPTY)
    add_date = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        d = dict(UserStatus.choices)
        name = d[self.status]
        return name

    def __str__(self):
        return self.user.username

class TutorStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    EMPTY = 'E'
    status = models.CharField(max_length=1,
            choices=UserStatus.choices,
            default=EMPTY)
    add_date = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        d = dict(UserStatus.choices)
        name = d[self.status]
        return name

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
