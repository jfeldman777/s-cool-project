from django import forms
from django.contrib.auth.models import User
from snow.models import UserProfile as Profile
from snow.models import Question

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #fields = ('bio', 'location', 'birth_date', 'picture','site')
        fields = ('bio', 'location', 'birth_date', 'site')

class QuestForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('txt','answer','picture')

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class VideoUploadForm(forms.Form):
    video = forms.FileField()

class AskStatus(forms.Form):
    role = forms.CharField()

class UpdCourse(forms.Form):
    name = forms.CharField(label='Title',
        widget=forms.TextInput(attrs={'size':70}),
        max_length=100)
    slides = forms.URLField(
        widget=forms.TextInput(attrs={'size':50}))
    pass



class UpdLecture(forms.Form):
    name = forms.CharField(label='Lecture',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)
    txt = forms.CharField(widget=forms.Textarea)
    pass

class AddCourse(forms.Form):
    course = forms.CharField(label='course',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)

    slides = forms.URLField(
        widget=forms.TextInput(attrs={'size':50}))

    lec_1 = forms.CharField(label='lecture 1',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)
    lec_2 = forms.CharField(label='lecture 2',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)
    lec_3 = forms.CharField(label='lecture 3',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)
    lec_4 = forms.CharField(label='lecture 4',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)
    lec_5 = forms.CharField(label='lecture 5',
        widget=forms.TextInput(attrs={'size':100}),
        max_length=100)
    pass
