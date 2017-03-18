from django.shortcuts import render
from snow.models import UserProfile as Profile
from snow.models import ExpertStatus, TutorStatus

from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import UserForm, ProfileForm, ImageUploadForm, AskStatus
from django.contrib import messages
from django.utils.translation import gettext as _

def index(request):
    return render(request,"index.html")

def home(request):
    return render(request,"index.html")

@login_required
def my_room(request):
    obj, created = Profile.objects.get_or_create(user = request.user)
    return render(request,"my_room.html")

@login_required
def set_status(request, role):
    answer = 'something strange happens'
    adm = ' - администратор рассмотрит вашу просьбу и примет решение '
    if role == 'e':
        answer = 'вы попросили роль эксперта '
        e, e_created = ExpertStatus.objects.get_or_create(user=request.user)
        if e.status == 'E':
            e.status = 'A'
            e.save()
            answer = answer + adm


    if role == 't':
        answer = 'вы попросили роль тьютора '
        t, t_created = TutorStatus.objects.get_or_create(user=request.user)
        if t.status == 'E':
            t.status = 'A'
            t.save()
            answer = answer + adm

    return render(request,"set_status.html",{'answer':answer})

@login_required
def get_status(request):
    if request.method == 'POST':
        form = AskStatus(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role == 'E':
                e, e_created = ExpertStatus.objects.get_or_create(user=request.user)
                if e.status != 'G':
                    return render(request,"get_status.html")
            if role == 'T':
                t, t_created = TutorStatus.objects.get_or_create(user=request.user)
                if t.status != 'G':
                    return render(request,"get_status.html")

            m = Profile.objects.get(user=request.user)
            m.last_status = role
            m.save()
            return render(request,"hall.html")

        messages.error(request, _('Please correct the error below.'))
        return render(request,"hall.html")
    else:
        return render(request,"get_status.html")

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
