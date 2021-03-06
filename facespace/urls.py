from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve
import settings

urlpatterns = patterns('',
    url(r'^$', 'frontend.views.index', name='index'),
    url(r'^about/$', 'frontend.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', 'api.views.api', name='api'),
    url(r'^bid/(\d+)/$', 'frontend.views.bid', name='bid'),
    url(r'^interest/(\d+)/$', 'frontend.views.interest', name='interest'),
    url(r'^create_interest/$', 'frontend.views.create_interest', name='create_interest'),
    url(r'^create_ad/$', 'frontend.views.create_ad', name='create_ad'),
    url(r'^profile/([a-zA-Z0-9.]+)/$', 'frontend.views.profile', name='profile'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^search/$', 'frontend.views.search', name='search'),
    url(r'^post_status/$', 'backend.views.post_status', name="post_status"),
    url(r'^upload/$', 'backend.views.upload', name="upload"),
    url(r'^upload_ad_pic/$', 'backend.views.upload', name="upload_ad_pic"),
    url(r'^friend/([0-9]+)/$', 'backend.views.friend', name="friend"),
    url(r'^romance_up/([0-9]+)/$', 'backend.views.romance_up', name="romance_up"),
    url(r'^romance_down/([0-9]+)/$', 'backend.views.romance_down', name="romance_down"),
    url(r'^confirm/([0-9]+)/$', 'backend.views.confirm', name="confirm"),
    url(r'^confirm_romance/([0-9]+)/([0-9]+)/$', 'backend.views.confirm_romance', name="confirm_romance"),
    url(r'^confirm_username/([a-zA-Z0-9.]+)/$', 'backend.views.confirm_username', name="confirm_username"),
    url(r'^register/$', 'backend.views.register', name="register"),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
)
