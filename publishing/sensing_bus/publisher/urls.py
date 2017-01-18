from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^visualize/', views.visualize, name='visualize'),
    url(r'^docs/', views.docs, name='docs'),
]
