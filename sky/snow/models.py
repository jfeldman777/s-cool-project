from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    story = models.TextField()
    is_student = models.BooleanField(blank=False)
    is_tutor = models.BooleanField(blank=False)
    is_expert = models.BooleanField(blank=False)
    is_tech = models.BooleanField(blank=False)
    is_god = models.BooleanField(blank=False)
    
    def __str__(self):
        return self.user.username