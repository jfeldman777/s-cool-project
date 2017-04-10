from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect

from django.contrib.auth.models import User
from snow.models import TutorStatus, UserProfile, Course
from .models import StudentTutorContract
from .forms import BookSearch

from django.db.models import Q

def book_search(request):
    form = BookSearch(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        in_title = form.cleaned_data['in_title']
        kw_after = form.cleaned_data['kw_after']

        if in_title == '' and kw_after == '':
            qset = Course.objects.all()
        elif kw_after == '':
            qset = Course.objects.filter(name__icontains=in_title)
        elif in_title == '':
            qset = Course.objects.filter(kw_after__icontains=kw_after)
        else:
            qset = Course.objects.filter(\
                Q(name__contains=in_title)|
                Q(kw_after__contains=kw_after))

        form = BookSearch(initial={'in_title':in_title,
                        'kw_after':kw_after})

        d = {
        'qset':qset,
        'form':form
        }


        return render(request,"book_search.html",d)
    else:
        form = BookSearch()
        d = {
        'form':form
        }
    return render(request,"book_search.html",d)

def t2s(request):
    d = {}
    return render(request,"tutor/t2s.html",d)

def s2t(request):
    tuts = TutorStatus.objects.all().exclude(user_id=request.user.id)
    d = {'qs':tuts}
    return render(request,"tutor/s2t.html",d)

def v_card_s(request, u_id):
    pf = UserProfile.objects.get(user_id=u_id)
    d = {'pf':pf,
    }
    return render(request,"tutor/v_card_s.html",d)

def v_card(request, u_id):
    pf = UserProfile.objects.get(user_id=u_id)
    created = True

    try:
        contract = StudentTutorContract.objects.get(\
            student_id = request.user.id, tutor_id = u_id)

    except:
        created = False
    d = {'pf':pf,
        'contract':contract
    }

    return render(request,"tutor/v_card.html",d)


def t2s_no(request,u_id):
    contract = StudentTutorContract.objects.get(\
            tutor_id = request.user.id, student_id = u_id)
    contract.tutor_yes = False
    contract.save()
    return redirect("/hall/")

def t2s_pro(request,u_id):
    contract = StudentTutorContract.objects.get(\
            tutor_id = request.user.id, student_id = u_id)
    contract.tutor_yes = True
    contract.save()
    return redirect("/hall/")

def s2t_pro(request, u_id):
    tutor = User.objects.get(id = u_id)
    d = {
        'tutor':tutor,
    }
    return render(request,"tutor/s2t_pro.html",d)

def s2t_no(request,u_id):
    contract = StudentTutorContract.objects.get(\
            student_id = request.user.id, tutor_id = u_id)

    contract.student_yes = False
    contract.save()

    messages.info(request, _('Вы отказались от сотрудничества'))
    return redirect("/hall/")

def s2t_pro_send(request,u_id):
    contract,created = StudentTutorContract.objects.get_or_create(\
            student_id = request.user.id, tutor_id = u_id)

    contract.student_yes = True
    contract.save()

    messages.info(request, _('Заявка отправлена'))
    return redirect("/hall/")
