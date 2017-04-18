from django import forms
from django.forms import ClearableFileInput
from django.contrib.admin import widgets
from django.contrib.auth.models import User

from .models import Lab

from django.contrib.admin.widgets import AdminDateWidget,  AdminTimeWidget, AdminSplitDateTime

class LabSearchForm(forms.Form):
    d_begin = forms.DateField(widget=widgets.AdminDateWidget(),label='начало')
    d_end = forms.DateField(widget=widgets.AdminDateWidget(),label='окончание')


class LabForm(forms.ModelForm):
    t_begin = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    t_end = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    class Meta:
        model = Lab
        fields = (
            'name','description','t_begin','t_end','address',
        )
        labels = {
            'name':'Название мероприятия',
            'description':'Описание мероприятия',
            't_begin':'Начало',
            't_end':'Окончание',
            'address':'Адрес',
        }
