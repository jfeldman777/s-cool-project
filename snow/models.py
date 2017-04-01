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

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slides = models.URLField(null=True, blank=False)

    approved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    video = fields.FileField(null=True)
    txt = models.TextField(max_length=300, blank=True)

    NUMBER = (
        ('0', 'Digest'),
        ('1', 'N1'),
        ('2', 'N2'),
        ('3', 'N3'),
        ('4', 'N4'),
        ('5', 'N5'),
    )
    number = models.CharField(
        max_length=1,
        choices=NUMBER,
        default='0',
    )
    def __str__(self):

        return self.name

class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    IN_OUT = (
        ('0','IN'),
        ('1','OUT')
    )
    in_out = models.CharField(
        max_length=1,
        choices=IN_OUT,
        default='0',
    )
    NUMBER = (
        ('1', 'N1'),
        ('2', 'N2'),
        ('3', 'N3'),
        ('4', 'N4'),
        ('5', 'N5'),
    )
    number = models.CharField(
        max_length=1,
        choices=NUMBER,
        default='0',
    )
    picture = fields.ImageField(null=True);
    txt = models.TextField(max_length=300, null=True)
    answer = models.IntegerField(null=True)

    def __str__(self):
        return self.txt

class ExamRecord(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    in_0 = models.BooleanField(default = False)
    out_0 = models.BooleanField(default = False)

    in_1 = models.BooleanField(default = False)
    out_1 = models.BooleanField(default = False)

    in_2 = models.BooleanField(default = False)
    out_2 = models.BooleanField(default = False)

    in_3 = models.BooleanField(default = False)
    out_3 = models.BooleanField(default = False)

    in_4 = models.BooleanField(default = False)
    out_4 = models.BooleanField(default = False)

    in_5 = models.BooleanField(default = False)
    out_5 = models.BooleanField(default = False)

    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student) + '@' + str(self.course)
