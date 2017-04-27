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

from snow.views import exam_qa_form, all_courses, course_s, keywords
from snow.views import create_crs, lecture, upd_crs, exam, enroll_me
from snow.views import ex_fwd, ex_back, exam_pic_form, upd_lecture
from snow.views import course, upd_video, upd_crs_video, show_video
from snow.views import crs_up, crs_down, crs_rec, final_test_wrn
from snow.views import crs_demo, rec2page, rec2back, rec2fwd, final_test

from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

from django.conf import settings
from django.conf.urls.static import static

from django.views.i18n import javascript_catalog

urlpatterns = []

if settings.DEBUG:#в этом режиме медиафайлы берутся из статической папки MEDIA
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/jsi18n', javascript_catalog, name='jsi18n'),

    url(r'^wiz/',include('wiz.urls')),
    url(r'^arc/',include('arc.urls')),
    url(r'^tut/',include('rain.urls')),

    url(r'^rec2fwd/(?P<crs>\d+)/', rec2fwd, name="rec2fwd"),
    url(r'^rec2back/(?P<crs>\d+)/', rec2back, name="rec2back"),
    url(r'^rec2page/(?P<rec>\d+)/', rec2page, name="rec2page"),


    url(r'^hall/(?P<lat>\d+\.\d+)/(?P<lng>\d+\.\d+)/', hall, name="hall"),
    url(r'^hall/', hall, name="hall"),


    url(r'^my_room/', my_room, name="my_room"),
    url(r'^edit_profile/', edit_profile, name="edit_profile"),
    url(r'^edit_pic/', edit_pic, name="edit_pic"),
    url(r'^get_status/', get_status, name="get_status"),
    url(r'^set_status/(?P<role>[etaw]{1})', set_status, name="set_status"),

    url(r'^create_crs/', create_crs, name="create_crs"),
    url(r'^upd_crs/(?P<crs>\d+)/', upd_crs, name="upd_crs"),
    url(r'^final_test_wrn/(?P<crs>\d+)/', final_test_wrn, name="final_test_wrn"),
    url(r'^final_test/(?P<crs>\d+)/', final_test, name="final_test"),

    url(r'^upd_lecture/(?P<crs>\d+)/(?P<lec>\d+)/', upd_lecture, name="upd_lecture"),
    url(r'^upd_video/(?P<crs>\d+)/(?P<lec>\d+)/', upd_video, name="upd_video"),
    url(r'^upd_crs_video/(?P<crs>\d+)/', upd_crs_video, name="upd_crs_video"),
    url(r'^show_video/(?P<crs>\d+)/(?P<lec>\d+)/', show_video, name="show_video"),

    url(r'^all_courses/', all_courses, name="all_courses"),

    url(r'^enroll_me/(?P<crs>\d+)', enroll_me, name="enroll_me"),
    url(r'^course_s/(?P<crs>\d+)', course_s, name="course_s"),
    url(r'^keywords/(?P<crs>\d+)', keywords, name="keywords"),

    url(r'^crs_up/(?P<crs>\d+)/', crs_up, name="crs_up"),
    url(r'^crs_down/(?P<crs>\d+)/', crs_down, name="crs_down"),

    url(r'^crs_demo/(?P<crs>\d+)/', crs_demo, name="crs_demo"),
    url(r'^crs_rec/(?P<crs>\d+)/', crs_rec, name="crs_rec"),

    url(r'^course/(?P<crs>\d+)', course, name="course"),
    url(r'^lecture/(?P<crs>\d+)/(?P<lec>\d+)', lecture, name="lecture"),
    url(r'^exam/(?P<crs>\d+)/(?P<lec>\d+)/(?P<inout>[01]{1})', exam, name="exam"),

    url(r'^ex_fwd/(?P<lec>\d+)/(?P<inout>[01]{1})', ex_fwd, name="ex_fwd"),
    url(r'^ex_back/(?P<lec>\d+)/(?P<inout>[01]{1})', ex_back, name="ex_back"),


    url(r'^exam_qa_form/(?P<lec>\d+)/(?P<inout>[01]{1})/(?P<num>\d+)',
                        exam_qa_form, name="exam_qa_form"),

    url(r'^exam_pic_form/(?P<lec>\d+)/(?P<inout>[01]{1})/(?P<num>\d+)',
                        exam_pic_form, name="exam_pic_form"),

    url(r'^accounts/profile/', home, name="home"),
    #по этому адресу вы будете отправлены при активации аккаунта линком из почты
    url(r'^register/$',  #заполните эту форму для регистрации
        RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),

    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    #тут лежат разные дополнительные возможности пакета регистрации -
    #вроде "хочу восстановить забытый пароль" - не проверено пока

    url(r'^', index, name="index"),#все остальные неотработанные линки сваливаются сюда
]
