from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from sky.forms import AddCourse, UpdLecture, VideoUploadForm, UpdCourse
from sky.forms import QuestForm

from .models import Course
from .models import Lecture
from .models import Question
from .models import ExamRecord
from .models import UserProfile

from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _

def crs_rec(request,crs):
    course = Course.objects.get(id=crs)
    lec_05 = [
        Lecture.objects.get(course = crs,number='0'),
        Lecture.objects.get(course = crs,number='1'),
        Lecture.objects.get(course = crs,number='2'),
        Lecture.objects.get(course = crs,number='3'),
        Lecture.objects.get(course = crs,number='4'),
        Lecture.objects.get(course = crs,number='5'),
        ]
    d = {
        'lec_05':lec_05,
        'course':course
    }
    return render(request,'student/crs_rec.html',d)

def crs_demo(request,crs):
    course = Course.objects.get(id=crs)
    profile = UserProfile.objects.get(user=course.user)
    first_name = User.objects.get(id=profile.user.id).first_name
    last_name = User.objects.get(id=profile.user.id).last_name
    lec_05 = [
        Lecture.objects.get(course = crs,number='0'),
        Lecture.objects.get(course = crs,number='1'),
        Lecture.objects.get(course = crs,number='2'),
        Lecture.objects.get(course = crs,number='3'),
        Lecture.objects.get(course = crs,number='4'),
        Lecture.objects.get(course = crs,number='5'),
        ]
    d = {
        'course':course,
        'profile':profile,
        'first_name':first_name,
        'last_name':last_name,
        'lec_05':lec_05,
    }
    return render(request,'student/crs_demo.html',d)

def crs_down(request, crs):
    course = Course.objects.get(id=crs)
    stu_crs = ExamRecord.objects.get(student = request.user,
                course = course)

    stu_crs.active = False
    stu_crs.save()
    return render(request,"student/enrolled.html",
            {
            'started':'long ago',
            'course':course
            })

def crs_up(request, crs):
    return enroll_me(request,crs)

def enroll_me(request,crs):
    course = Course.objects.get(id=crs)
    stu_crs, created = ExamRecord.objects.get_or_create(student = request.user,
                course = course)
    if created:
        return render(request,"student/enrolled.html",
            {
            'started':'just now',
            'course':course
            })
    else:
        stu_crs.active = True
        stu_crs.save()
        return render(request,"student/enrolled.html",
            {
            'started':'again',
            'course':course
            })

def course_s(request,crs):
    return course(request,crs,'student/course_s.html')

def all_courses(request):
    qset = Course.objects.filter(approved=True)
    return render(request,'student/all_courses.html',{'qset':qset})

def exam_qa_form(request,lec,inout,num):
    lecture = Lecture.objects.get(id=lec)
    course = Course.objects.get(id = lecture.course.id)
    if course.user != request.user:
        raise Http404("Not yours")
    m,created = Question.objects.get_or_create(lecture=lecture,in_out=inout,number=num)
    form = QuestForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        m.txt = form.cleaned_data['txt']
        m.answer = form.cleaned_data['answer']
        m.picture = form.cleaned_data['picture']
        m.save()
        messages.success(request, _('The data were successfully updated!'))
        return exam(request,course.id,lec,inout)
    else:
        form = QuestForm(instance=m)
        d = {'lecture':lecture,
            'course':course,
            'inout':inout,
            'number':num,
            'form':form
            }
        return render(request, 'lecture/exam_qa_form.html',d)

def exam(request,crs,lec,inout):
    course = Course.objects.get(id=crs)
    lecture = Lecture.objects.get(id=lec)
    if course.user != request.user:
        raise Http404("Not yours")
    q1,c1 = Question.objects.get_or_create(lecture=lecture,in_out=inout,number='1')
    q2,c2 = Question.objects.get_or_create(lecture=lecture,in_out=inout,number='2')
    q3,c3 = Question.objects.get_or_create(lecture=lecture,in_out=inout,number='3')
    q4,c4 = Question.objects.get_or_create(lecture=lecture,in_out=inout,number='4')
    q5,c5 = Question.objects.get_or_create(lecture=lecture,in_out=inout,number='5')
    q15 =  ((q1,1),
            (q2,2),
            (q3,3),
            (q4,4),
            (q5,5))
    return render(request,'lecture/exam.html',
        {
         'q15':q15,
         'course':course,
         'lecture':lecture,
         'inout':inout,
         }
    )

def show_video(request,crs,lec):
    course = Course.objects.get(id=crs)
    lecture = Lecture.objects.get(id=lec)
    d = {
        'course': course,
        'lecture':lecture,
        }
    return render(request,'lecture/show_video.html',d)

def upd_lecture(request,crs,lec):
    course = Course.objects.get(id=crs)
    if course.user != request.user:
        raise Http404("Not yours")
    lecture = Lecture.objects.get(id=lec)
    form = UpdLecture(request.POST or None)
    if form.is_valid():
        lecture.name = form.cleaned_data['name']
        lecture.txt = form.cleaned_data['txt']
        lecture.save()
        messages.success(request,
            _('The lecture was successfully updated!'))
        return render(request,'lecture/lecture.html',
                        {'lecture':lecture,
                        'course':course,
                        })
    else:
        d = {
            'name':lecture.name,
            'txt':lecture.txt,
        }
        form = UpdLecture(d)
        return render(request,
                'lecture/upd_lecture.html',{
                    'form':form,
                    'lecture':lecture,
                    'course':course,
                })

def upd_video(request,crs,lec):
    course = Course.objects.get(id=crs)
    if course.user != request.user:
        raise Http404("Not yours")
    lecture = Lecture.objects.get(id=lec)
    form = VideoUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        lecture.video = form.cleaned_data['video']
        lecture.save()
        messages.success(request, _('Your video was successfully updated!'))
        return redirect('/course/'+str(crs))
    else:
        return render(request,'lecture/upd_video.html',{
            'form':form,
            'course':course,
            'lecture':lecture,
        })

def upd_crs(request,crs):
    course = Course.objects.get(id=crs)
    if course.user != request.user:
        raise Http404("Not yours")
    form = UpdCourse(request.POST or None)
    if form.is_valid():
        course.name = form.cleaned_data['name']
        course.slides = form.cleaned_data['slides']
        course.save()

        messages.success(request,
            _('The course was successfully updated!'))
        return redirect('/course/'+crs)
    else:

        d = {
            'name':course.name,
            'slides':course.slides,
        }
        form = UpdCourse(d)
        return render(request,
                'lecture/upd_crs.html',{
                    'form':form,
                    'course':course,
                })

def create_crs(request):
    form = AddCourse(request.POST or None)
    if form.is_valid():
        user = request.user
        c_name = form.cleaned_data['course']
        slides = form.cleaned_data['slides']

        course = Course(
            user = user,
            name = c_name,
            slides = slides)
        course.save()

        lec_0 = Lecture(
            course = course,
            name = c_name,
            number = '0')
        lec_0.save()

        name_1 = form.cleaned_data['lec_1']
        lec_1 = Lecture(
            course = course,
            name = name_1,
            number = '1')
        lec_1.save()

        name_2 = form.cleaned_data['lec_2']
        lec_2 = Lecture(
            course = course,
            name = name_2,
            number = '2')
        lec_2.save()

        name_3= form.cleaned_data['lec_3']
        lec_3 = Lecture(
            course = course,
            name = name_3,
            number = '3')
        lec_3.save()

        name_4 = form.cleaned_data['lec_4']
        lec_4 = Lecture(
            course = course,
            name = name_4,
            number = '4')
        lec_4.save()

        name_5 = form.cleaned_data['lec_5']
        lec_5 = Lecture(
            course = course,
            name = name_5,
            number = '5')
        lec_5.save()

        messages.success(request,
            _('New course was successfully created!'))

        return redirect('/hall/')
    else:
        return render(request, "create_crs.html", {'form':form})

def course(request,crs,templ="course.html"):
    course = Course.objects.get(id=crs)
    lec_05 = [
        Lecture.objects.get(course = crs,number='0'),
        Lecture.objects.get(course = crs,number='1'),
        Lecture.objects.get(course = crs,number='2'),
        Lecture.objects.get(course = crs,number='3'),
        Lecture.objects.get(course = crs,number='4'),
        Lecture.objects.get(course = crs,number='5'),
        ]
    return render(request,templ,{
            'lec_05':lec_05,
            'course':course,
        }
    )

def lecture(request,crs,lec):
    course = Course.objects.get(id=crs)
    lecture = Lecture.objects.get(id=lec)
    return render(request,'lecture/lecture.html',
                    {'lecture':lecture,
                    'course':course,
                    })
