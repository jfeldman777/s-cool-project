from django.shortcuts import render
from django.shortcuts import redirect

from .forms import CatForm
from .models import Cat
from snow.models import Course, UserProfile

from django.contrib import messages
from django.utils.translation import gettext as _

def attach(request,crs,cat):
    my_cat = Cat.objects.get(id=cat)
    my_cat.books.add(crs)
    my_cat.save()
    return redirect("/arc/c2c/" + crs + "/")

def detach(request,crs,cat):
    my_cat = Cat.objects.get(id=cat)
    my_cat.books.remove(crs)
    my_cat.save()
    return redirect("/arc/c2c/" + crs + "/")

def c2c(request,crs):
    course = Course.objects.get(id=crs)
    expert = UserProfile.objects.get(user_id = course.user_id)

    q1 = Cat.objects.filter(books = course).order_by('name')
    q2 = Cat.objects.all().exclude(books = course).order_by('name')

    d = {
        'expert':expert,
        'course':course,
        'q1':q1,
        'q2':q2,
    }
    return render(request,'arc/c2c.html',d)

def new_cat(request):
    form = CatForm(request.POST or None)
    if form.is_valid():
        cat = Cat()
        cat.name = form.cleaned_data['name']
        try:
            cat.save()
            messages.success(request,
            _('The data were successfully updated!'))
        except:
            messages.warning(request,
            _('creation fails - probably the name is not unique?'))
        return redirect('/hall/')
    else:
        form = CatForm()
        d = {
        'form':form
        }
        return render(request,'arc/new_cat.html',d)
