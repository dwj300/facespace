from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^frontend/', include('frontend.urls', namespace='frontend', app_name='frontend')),
    url(r'^api/', include('api.urls', namespace='api', app_name='api')),
    url(r'^$', 'frontend.views.index', name='index'),
)
