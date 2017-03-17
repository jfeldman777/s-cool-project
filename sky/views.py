from django.shortcuts import render
from snow.models import UserProfile as Profile
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import UserForm, ProfileForm, ImageUploadForm
from django.contrib import messages
from django.utils.translation import gettext as _

def index(request):
    return render(request,"index.html")

def home(request):
    return render(request,"index.html")

def my_room(request):
    obj, created = Profile.objects.get_or_create(user = request.user)
    return render(request,"my_room.html")

@login_required
def hall(request):
    return render(request,"hall.html")

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
            return my_room(request)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
    })

@login_required
@transaction.atomic
def edit_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Profile.objects.get(user=request.user)
            m.picture = form.cleaned_data['image']
            m.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return my_room(request)
        else:
            messages.error(request, _('Please correct the error below.'))
            return my_room(request)
    return render(request, 'edit_pic.html')
