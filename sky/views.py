from django.shortcuts import render
from snow.models import UserProfile as Profile
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.utils.translation import gettext as _

def index(request):
    return render(request,"index.html")

def home(request):
    return render(request,"index.html")

def my_room(request):
    obj, created = Profile.objects.get_or_create(user = request.user)
    return render(request,"my_room.html")

#edit_profile
@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return my_room(request)
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
    })
