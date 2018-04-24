from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^dashboard$', views.dash),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^wish_items/(?P<id>\d+)$', views.display_item),
    url(r'^wish_items/create$', views.create),
    url(r'^wish_items/create/process$', views.process),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete)
]