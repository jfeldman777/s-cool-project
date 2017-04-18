from django.shortcuts import render
from .models import Lab
from .forms import LabForm, LabSearchForm
from sky.views import hall
from datetime import datetime, timedelta

def lab_search(request):
    form = LabSearchForm(request.POST or None)
    if form.is_valid():
        d_begin = form.cleaned_data['d_begin']
        d_end = form.cleaned_data['d_end']

        qs = Lab.objects.filter\
    (t_begin__gte=d_begin,t_begin__lte=d_end+timedelta(days=1)).order_by('name')

    else:
        form = LabSearchForm()
        qs = Lab.objects.all().order_by('name')

    d = {
    'qs':qs,
    'form':form
        }
    return render(request,"wiz/lab_search.html",d)

def show_lab(request,lab):
    my_lab = Lab.objects.get(id=lab)
    d = {
        'lab':my_lab
    }
    return render(request,"wiz/show_lab.html",d)

def new_lab(request):
    form = LabForm(request.POST or None)
    if form.is_valid():
        lab = Lab()
        lab.teacher = request.user
        lab.name = form.cleaned_data['name']
        lab.description = form.cleaned_data['description']
        lab.t_begin = form.cleaned_data['t_begin']
        lab.t_end = form.cleaned_data['t_end']
        lab.address = form.cleaned_data['address']
        lab.save()
        return hall(request)
    else:
        form = LabForm()
        pass

        d = {
            'form':form,
        }
        return render(request,"wiz/new_lab.html",d)
