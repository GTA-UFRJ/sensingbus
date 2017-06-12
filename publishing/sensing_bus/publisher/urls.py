from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^visualize/', views.visualize, name='visualize'),
    url(r'^docs/',  views.docs, name='docs'),
    url(r'^measurements/$',views.measurement_list),
    ##Uncommenting the next line creates an unprotected url, good for testing
    #url(r'^measurements_batch/$',views.measurement_batch_list), 
    url(r'^measurements_batch_sec/$',views.measurement_batch_list),
    url(r'^measurements/(?P<pk>[0-9]+)/$', views.measurement_detail),
    url(r'^zip_measurements_batch_sec/$',views.zip_measurement_batch_list)
]