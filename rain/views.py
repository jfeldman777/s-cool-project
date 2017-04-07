from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect


def t2s(request):
    print('t2s')
    return render(request,"tutor/t2s.html")

def s2t(request):
    print('s2t')
    return render(request,"tutor/s2t.html")
