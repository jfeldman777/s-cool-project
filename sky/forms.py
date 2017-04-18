from django import forms
from django.forms import ClearableFileInput
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from snow.models import UserProfile as Profile
from snow.models import Question, Course

from django.contrib.admin.widgets import AdminDateWidget,  AdminTimeWidget, AdminSplitDateTime
#from django.forms.widgets import DateInput

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class KwForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('kw_before','kw_after')

#from functools import partial
#DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class ProfileForm(forms.ModelForm):
    site = forms.CharField(required=False)
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'site')
        labels = {
            'birth_date': 'дата рождения',
            'bio':'о себе',
            'location':'город (страна)',
        }
        #widgets = {'birth_date':AdminDateWidget(),}


class QuestForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('txt','answer')

class BigQuestForm(forms.Form):
        txt = forms.CharField(disabled=True)
        answer = forms.IntegerField(required=False)


class CustomClearableFileInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )

    template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        required=False, widget=CustomClearableFileInput
        )

class VideoUploadForm(forms.Form):
    video = forms.FileField(
        required=False, widget=CustomClearableFileInput
    )

class AskStatus(forms.Form):
    role = forms.CharField()

class UpdCourse(forms.Form):
    name = forms.CharField(label='Title',
        widget=forms.TextInput(attrs={'size':70}),
        max_length=100)
    slides = forms.URLField(
        widget=forms.TextInput(attrs={'size':50}))
    completed = forms.BooleanField()
    pass

class TestDone(forms.Form):
    a_1 = forms.IntegerField()
    a_2 = forms.IntegerField()
    a_3 = forms.IntegerField()
    a_4 = forms.IntegerField()
    a_5 = forms.IntegerField()

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
