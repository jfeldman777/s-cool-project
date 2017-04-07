from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from django.forms import formset_factory

from sky.forms import AddCourse, UpdLecture, VideoUploadForm, UpdCourse
from sky.forms import QuestForm, BigQuestForm, \
        TestDone, ImageUploadForm, KwForm

from .models import Course
from .models import Lecture
from .models import Question
from .models import ExamRecord
from .models import UserProfile

from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
#from django.forms.formsets import formset_factory

CURRENT_PAGE = [
    'вы зарегистрировались на этот курс',#0
    'Лекция №1: вы приступили к сдаче входного теста',#1
    'Лекция №1: вы приступили к просмотру видео',#2
    'Лекция №1: вы приступили к сдаче вЫходного теста',#3
    'Лекция №2: вы приступили к сдаче входного теста',#4
    'Лекция №2: вы приступили к просмотру видео',#5
    'Лекция №2: вы приступили к сдаче вЫходного теста',#6
    'Лекция №3: вы приступили к сдаче входного теста',#7
    'Лекция №3: вы приступили к просмотру видео',#8
    'Лекция №3: вы приступили к сдаче вЫходного теста',#9
    'Лекция №4: вы приступили к сдаче входного теста',#10
    'Лекция №4: вы приступили к просмотру видео',#11
    'Лекция №4: вы приступили к сдаче вЫходного теста',#12
    'Лекция №5: вы приступили к сдаче входного теста',#13
    'Лекция №5: вы приступили к просмотру видео',#14
    'Лекция №5: вы приступили к сдаче вЫходного теста',#15
    'вы приступили к сдаче финального теста',#16
    'вы сдали финальный тест - курс закрыт'#17
]

def page2tuple(page):
    lec = (page+2) // 3
    sec = (page+2) % 3
    return (lec,sec)

def rec2exam(lec,inout):
    qset = Question.objects.filter(lecture=lec,in_out=inout).order_by('number')
    q = list(qset)
    return q

def rec2back(request,crs):
    record = ExamRecord.objects.get(course_id=crs,student=request.user)
    page = record.current
    if page > 1:
        record.current = page-1
        record.save()
    return rec2page(request,record.id)

def rec2fwd(request,crs):
    course = Course.objects.get(id=crs)
    record = ExamRecord.objects.get(course_id=course.id,student_id=request.user)
    page = record.current
    lec,sec = page2tuple(page)

    lecture = Lecture.objects.get(course_id=crs,number=str(lec))

    if sec == 0:
        inout = '0'
    else:
        inout = '1'

    if request.method == 'POST':
        form = TestDone(request.POST)
        if form.is_valid() or True:

            a1 = form.cleaned_data['a_1']
            a2 = form.cleaned_data['a_2']
            a3 = form.cleaned_data['a_3']
            a4 = form.cleaned_data['a_4']
            a5 = form.cleaned_data['a_5']

            q1 = Question.objects.get(lecture=lecture,in_out=inout,number='1')
            q2 = Question.objects.get(lecture=lecture,in_out=inout,number='2')
            q3 = Question.objects.get(lecture=lecture,in_out=inout,number='3')
            q4 = Question.objects.get(lecture=lecture,in_out=inout,number='4')
            q5 = Question.objects.get(lecture=lecture,in_out=inout,number='5')


            if q1.answer == a1 and q2.answer == a2 and \
                q3.answer == a3 and q4.answer == a4 and q5.answer == a5:
                record.current = page+1
                record.save()
                messages.info(request, \
                _('Поздравляем, тест сдан, движемся дальше'))
            elif sec > 0 :
                record.current = page-1
                record.save()
                messages.info(request, \
                _('К сожалению, тест провален, смотрим видео еще раз'))
            else:
                messages.info(request, \
                _('К сожалению, тест провален, вы можете повторить попытку, \
                или выбрать другой курс, более простой'))
        else:
            messages.error(request, \
            _('Необходимо заполнить все поля'))
        return rec2page(request,record.id)
    else:
        record.current = page+1
    record.save()
    return rec2page(request,record.id)

def page_q(request,crs,lec,inout,page):
    q1 = Question.objects.get(lecture=lec,in_out=inout,number='1')
    q2 = Question.objects.get(lecture=lec,in_out=inout,number='2')
    q3 = Question.objects.get(lecture=lec,in_out=inout,number='3')
    q4 = Question.objects.get(lecture=lec,in_out=inout,number='4')
    q5 = Question.objects.get(lecture=lec,in_out=inout,number='5')

    form = TestDone();
    d = {
        'form':form,
        'p1':q1.picture or None,
        'p2':q2.picture or None,
        'p3':q3.picture or None,
        'p4':q4.picture or None,
        'p5':q5.picture or None,
        't1':q1.txt,
        't2':q2.txt,
        't3':q3.txt,
        't4':q4.txt,
        't5':q5.txt,
        'crs':crs,
        'current':CURRENT_PAGE[page],
        }
    return render(request,'student/page_q.html',d)

def page_v(request,crs,lec,page):
    lecture = Lecture.objects.get(id=lec)
    course = Course.objects.get(id=crs)
    d = {
        'course':course,
        'lecture':lecture,
        'page':page
    }
    return render(request,'student/page_v.html',d)


def rec2page(request,rec):
    record = ExamRecord.objects.get(id=rec)
    page = record.current
    if page == 0:
        page = 1
    crs = record.course_id

    lec_num,sec = page2tuple(page)

    if lec_num > 5:
        return final_test(request,crs)


    lecture = Lecture.objects.get(course_id=crs,number=lec_num)
    lec = lecture.id

    if sec == 1:
        return page_v(request,crs,lec,page)
    elif sec == 0:
        return page_q(request,crs,lec,'0',page)
    else:
        return page_q(request,crs,lec,'1',page)

def final_test(request,crs):
    course = Course.objects.get(id=crs)
    rec = ExamRecord.objects.get(course=crs,student=request.user)
    rec.final_try_used = True
    rec.save()

    lec_15 = Lecture.objects.filter(course_id=crs).order_by('number')
    ls = list(lec_15)
    lx = [x.id for x in ls]
    z = []
    BigSet = formset_factory(BigQuestForm, extra=25)


    if request.method == 'POST':
        formset = BigSet(request.POST)
        print(formset.total_error_count())

        az = []
        n = 0
        for form in formset:
            p = n//5
            q = n%5
            n = n+1
            question = Question.objects.get(lecture_id=lx[p],\
                            number=str(q+1),in_out='1')
            try:
                a = form.cleaned_data['answer']
                if a != question.answer:
                    messages.info(request,\
                    _('Некоторые ответы неверны, незачет '))
                    return crs_demo(request,course.id)

            except:
                messages.info(request,\
                _('Некоторые вопросы не были отвечены, незачет '))
                return crs_demo(request,course.id)

        messages.info(request,\
        _('Поздравляю, вы сдали экзамен на отлично!'))

        rec.done = True
        rec.save()
        return hall(request)
    else:
        n=0
        data = {
            'form-TOTAL_FORMS': u'25',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'25',
        }
        formset = BigSet(data)
        for form in formset:
            p = n//5
            q = n%5
            n = n+1
            question = Question.objects.get(lecture_id=lx[p],\
                            number=str(q+1),in_out='1')

            if question.picture:
                pic = 'img src={0}'.format(question.picture.url)
            else:
                pic = 'br'
            form.initial = {'txt':question.txt}
            z.append((form,pic))

        d = {
            'course':course,
            'formset':formset,
            'z':z
        }
        return render(request,'student/final_test.html',d)

def keywords(request,crs):
    c = Course.objects.get(id=crs)
    form = KwForm(request.POST or None)
    if form.is_valid():
        c.kw_before = form.cleaned_data['kw_before']
        c.kw_after = form.cleaned_data['kw_after']
        c.save()
        messages.success(request, _('The data were successfully updated!'))
        return course(request,crs)
    else:
        form = KwForm(initial=
            {'kw_before':c.kw_before,'kw_after':c.kw_after})
        d = {
        'course':c,
        'form':form
        }
        return render(request,'lecture/keywords.html',d)

def final_test_wrn(request,crs):
    d = {'crs':crs}
    return render(request,'student/final_test_wrn.html',d)

def crs_rec(request,crs):
    rec = ExamRecord.objects.get(course=crs,student=request.user)
    page = rec.current
    course = Course.objects.get(id=crs)
    lec_15 = [
        Lecture.objects.get(course = crs,number='1'),
        Lecture.objects.get(course = crs,number='2'),
        Lecture.objects.get(course = crs,number='3'),
        Lecture.objects.get(course = crs,number='4'),
        Lecture.objects.get(course = crs,number='5'),
        ]
    d = {
        'lec_15':lec_15,
        'course':course,
        'current':CURRENT_PAGE[page],
        'rec':rec
    }
    return render(request,'student/crs_rec.html',d)

def crs_demo(request,crs):
    course = Course.objects.get(id=crs)
    profile = UserProfile.objects.get(user=course.user)
    first_name = User.objects.get(id=profile.user.id).first_name
    last_name = User.objects.get(id=profile.user.id).last_name
    lec_15 = [
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
        'lec_15':lec_15,
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

def exam_pic_form(request,lec,inout,num):
    lecture = Lecture.objects.get(id=lec)
    course = Course.objects.get(id = lecture.course.id)
    if course.user != request.user:
        raise Http404("Not yours")
    m,created = Question.objects.get_or_create(lecture=lecture,in_out=inout,number=num)
    form = ImageUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        m.picture = form.cleaned_data['image']
        m.save()
        messages.success(request, _('The data were successfully updated!'))
        return exam(request,course.id,lec,inout)
    else:
        form = ImageUploadForm(initial={'image':m.picture})
        d = {'lecture':lecture,
            'course':course,
            'inout':inout,
            'number':num,
            'form':form
            }
        return render(request, 'lecture/exam_pic_form.html',d)

def exam_qa_form(request,lec,inout,num):
    lecture = Lecture.objects.get(id=lec)
    course = Course.objects.get(id = lecture.course.id)
    if course.user != request.user:
        raise Http404("Not yours")
    m,created = Question.objects.get_or_create(lecture=lecture,in_out=inout,number=num)
    form = QuestForm(request.POST or None)
    if form.is_valid():
        m.txt = form.cleaned_data['txt']
        m.answer = form.cleaned_data['answer']
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

def ex_fwd(request,lec,inout):
    lecture = Lecture.objects.get(id=lec)
    crs = lecture.course_id
    num = int(lecture.number)

    if inout == '0':
        lecture2 = Lecture.objects.get(course_id=crs,number = lecture.number)
        return exam(request,crs,lecture2.id,'1')
    elif num == 5:
        return course(request,crs)
    else:
        lecture2 = Lecture.objects.get(course_id=crs,number = str(num+1))
        return exam(request,crs,lecture2.id,'0')

def ex_back(request,lec,inout):
    lecture = Lecture.objects.get(id=lec)
    crs = lecture.course_id
    num = int(lecture.number)

    if inout == '1':
        lecture2 = Lecture.objects.get(course_id=crs,number = lecture.number)
        return exam(request,crs,lecture2.id,'0')
    elif num == 0:
        return course(request,crs)
    else:
        lecture2 = Lecture.objects.get(course_id=crs,number = str(num-1))
        return exam(request,crs,lecture2.id,'1')

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

def show_crs_video(request,crs):
    course = Course.objects.get(id=crs)
    d = {
        'course': course,
        }
    return render(request,'lecture/show_crs_video.html',d)

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

def upd_crs_video(request,crs):
    course = Course.objects.get(id=crs)
    if course.user != request.user:
        raise Http404("Not yours")
    form = VideoUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        course.video = form.cleaned_data['video']
        course.save()
        messages.success(request, _('Your video was successfully updated!'))
        return redirect('/course/'+str(crs))
    else:
        form = VideoUploadForm(initial={'video':course.video})
        return render(request,'lecture/upd_crs_video.html',{
            'form':form,
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
        form = VideoUploadForm(initial={'video':lecture.video})
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
        course.completed = form.cleaned_data['completed']
        course.save()

        messages.success(request,
            _('The course was successfully updated!'))
        return redirect('/course/'+crs)
    else:

        d = {
            'name':course.name,
            'slides':course.slides,
            'completed':course.completed
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
    lec_15 = [
        Lecture.objects.get(course = crs,number='1'),
        Lecture.objects.get(course = crs,number='2'),
        Lecture.objects.get(course = crs,number='3'),
        Lecture.objects.get(course = crs,number='4'),
        Lecture.objects.get(course = crs,number='5'),
        ]
    return render(request,templ,{
            'lec_15':lec_15,
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
