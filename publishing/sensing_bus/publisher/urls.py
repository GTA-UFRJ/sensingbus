from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^visualize/', views.zz, name='visualize'),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^measurements/$',views.measurement_list),
    url(r'^measurements_batch/$',views.measurement_batch_list),
    url(r'^measurements_batch_sec/$',views.measurement_batch_list),
    url(r'^measurements/(?P<pk>[0-9]+)/$', views.measurement_detail),
]
