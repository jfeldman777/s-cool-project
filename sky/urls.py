"""sky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import index, home, my_room, edit_profile
from .views import hall, edit_pic, get_status, set_status
from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = []

if settings.DEBUG:#в этом режиме медиафайлы берутся из статической папки MEDIA
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    #панель администратора - для тех у кого есть права администратора
    url(r'^hall/', hall, name="hall"),
    url(r'^my_room/', my_room, name="my_room"),
    url(r'^edit_profile/', edit_profile, name="edit_profile"),
    url(r'^edit_pic/', edit_pic, name="edit_pic"),
    url(r'^get_status/', get_status, name="get_status"),
    url(r'^set_status/(?P<role>[et])', set_status, name="set_status"),
    #/edit_profile/

    url(r'^accounts/profile/', home, name="home"),
    #по этому адресу вы будете отправлены при активации аккаунта линком из почты

    url(r'^register/$',  #заполните эту форму для регистрации
        RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),

    url(r'^accounts/', include('registration.backends.hmac.urls')),
    #тут лежат разные дополнительные возможности пакета регистрации -
    #вроде "хочу восстановить забытый пароль" - не проверено пока

    url(r'^', include('django.contrib.auth.urls')),
    #тут лежат разные дополнительные возможности пакета регистрации -
    #вроде "хочу восстановить забытый пароль" - не проверено пока


    url(r'^', index, name="index"),#все остальные неотработанные линки сваливаются сюда
]
