from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve
import settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^frontend/', include('frontend.urls', namespace='frontend', app_name='frontend')),
    url(r'^api/', include('api.urls', namespace='api', app_name='api')),
    url(r'^interest/(\d+)/$','frontend.views.interest', name='interest'),
    url(r'^$', 'frontend.views.index', name='index'),
    url(r'^home/$', 'frontend.views.home', name='home'),
    url(r'^profile/([a-zA-Z0-9]+)/$', 'frontend.views.profile', name='profile'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
	url(r'^search/$', 'frontend.views.search', name='search'),
    url(r'^upload/$', 'backend.views.upload', name="upload"),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
)
