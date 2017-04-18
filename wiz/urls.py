from django.conf.urls import url,include
from .views import new_lab, show_lab, lab_search

urlpatterns = [
    url(r'^lab_search/', lab_search, name="lab_search"),
    url(r'^new_lab/', new_lab, name="new_lab"),
    url(r'^show_lab/(?P<lab>\d+)/', show_lab, name="show_lab"),
    ]
