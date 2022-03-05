from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.list, name='index'),
    path('upload', views.upload, name='upload'),
    path('list', views.list, name='list'),
    path('keys', views.keys, name='keys'),
    re_path('^object/(?P<id>[0-9a-f]{32})/?$', views.retrieve, name='retrieve'),
]