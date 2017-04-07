from django.conf.urls import url,include

from .views import t2s, s2t

urlpatterns = [
    url(r'^t2s', t2s, name="t2s"),
    url(r'^s2t', s2t, name="s2t"),

]
