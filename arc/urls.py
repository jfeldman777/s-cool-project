from django.conf.urls import url,include
from .views import new_cat, c2c, attach, detach

urlpatterns = [
    url(r'^new_cat/', new_cat, name="new_cat"),
    url(r'^c2c/(?P<crs>\d+)/', c2c, name="c2c"),
    url(r'^attach/(?P<crs>\d+)/(?P<cat>\d+)/', attach, name="attach"),
    url(r'^detach/(?P<crs>\d+)/(?P<cat>\d+)/', detach, name="detach"),
    ]
