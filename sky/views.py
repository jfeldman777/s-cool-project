from django.shortcuts import render
from snow.models import UserProfile as Profile
from snow.models import ExpertStatus, TutorStatus
from snow.models import Course, ExamRecord

from rain.models import StudentTutorContract

from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import UserForm, ProfileForm, ImageUploadForm, AskStatus
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect

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
    #if request.method == 'POST':
        form = AskStatus(request.POST or None)
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
            return redirect("/hall/")


        else:
            return render(request,"get_status.html")

@login_required
def hall(request):
    user = request.user
    qset = []
    try:
        role = user.userprofile.last_status
    except:
        messages.error(request, \
_('Прежде чем вас допустят в общий зал надо зайтив личный кабинет и заполнить личные данные'))
        return redirect('/')

    if role == 'E':
        q_approved = Course.objects.filter(user = user,approved=True)
        q_completed = Course.objects.filter(user = user,approved=False,completed=True)
        q_started = Course.objects.filter(user = user,approved=False,completed=False)
        q_common = Course.objects.exclude(user = user).filter(completed=True)

        d = {
            'q_approved':q_approved,
            'q_completed':q_completed,
            'q_started':q_started,
            'q_common':q_common
        }

        return render(request,"hall.html",d)

    elif role == 'T':
        qs11 = StudentTutorContract.objects.filter(\
                student_yes = True, tutor_yes = True)

        qs01 = StudentTutorContract.objects.filter(\
                student_yes = True, tutor_yes = False)

        qs10 = StudentTutorContract.objects.filter(\
            student_yes = False)

        d = {
        'qs11':qs11,
        'qs01':qs01,
        'qs10':qs10,
        }
        return render(request,"hall.html",d)

    elif role == 'S':
        qset5 = ExamRecord.objects.filter(student = user, done=True)
        p5 = [x['course_id'] for x in qset5.values()]
        list5 = list(qset5)

        qset1 = ExamRecord.objects.filter(student = user, active=True, done=False)
        p1 = [x['course_id'] for x in qset1.values()]

        qset2 = ExamRecord.objects.filter(student = user, active=False, done=False)
        p2 = [x['course_id'] for x in qset2.values()]

        qset3 = Course.objects.filter(approved = True)
        list3 = list(qset3)


        list4 = \
[x for x in list3 if x.id not in p1 if x.id not in p2 if x.id not in p5]
        list1 = [x for x in list3 if x.id in p1]
        list2 = [x for x in list3 if x.id in p2]

        return render(request,"hall.html",
            {
            'qset1':list1,'qset2':list2,'qset4':list4,'qset5':list5,
            })
    return render(request,"hall.html")
    #return redirect("/")

@login_required
@transaction.atomic
def edit_profile(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, instance=request.user.userprofile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, _('Your profile was successfully updated!'))
        return my_room(request)
    else:
        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
    })

@login_required
@transaction.atomic
def edit_pic(request):
    m,created = Profile.objects.get_or_create(user=request.user)
    form = ImageUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        m = Profile.objects.get(user=request.user)
        m.picture = form.cleaned_data['image']
        m.save()
        messages.success(request, _('Your profile was successfully updated!'))
        return my_room(request)
    else:
        form = ImageUploadForm(initial={'image':m.picture})
        return render(request, 'edit_pic.html',{'form':form})
