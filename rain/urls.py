from django.conf.urls import url,include

from .views import t2s, v_card_s, book_search,\
 s2t, v_card, s2t_pro, s2t_pro_send, t2s_pro, t2s_no, s2t_no

urlpatterns = [
    url(r'^t2s/', t2s, name="t2s"),
    url(r'^s2t/', s2t, name="s2t"),
    url(r'^book_search/', book_search, name="book_search"),

    url(r'^v_card/(?P<u_id>\d+)/', v_card, name="v_card"),
    url(r'^v_card_s/(?P<u_id>\d+)/', v_card_s, name="v_card_s"),
    url(r'^s2t_pro/(?P<u_id>\d+)/', s2t_pro, name="s2t_pro"),
    url(r'^s2t_pro_send/(?P<u_id>\d+)/', s2t_pro_send, name="s2t_pro_send"),
    url(r'^t2s_pro/(?P<u_id>\d+)/',t2s_pro, name="t2s_pro"),
    url(r'^t2s_no/(?P<u_id>\d+)/',t2s_no, name="t2s_no"),
    url(r'^s2t_no/(?P<u_id>\d+)/',s2t_no, name="s2t_no"),
]
