from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wall$', views.wall),
    url(r'^logout_view$', views.logout_view),
    url(r'^message$', views.message),
    url(r'^comment/(?P<id>[0-9]+)$', views.comment),
    url(r'^delete_message/(?P<id>[0-9]+)$', views.delete_message)
]