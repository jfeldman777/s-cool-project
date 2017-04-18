from django import forms
from django.contrib import admin
from .models import Lab
from easy_maps.widgets import AddressWithMapWidget

class LabAdmin(admin.ModelAdmin):
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }

admin.site.register(Lab, LabAdmin)
