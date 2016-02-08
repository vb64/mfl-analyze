from django.conf.urls.defaults import *
from django.http import HttpResponse

import views

urlpatterns = patterns('',
  url(r'robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
  url(r'^api/put$', views.data_put, name='api_put'),
  url(r'^api/get/(?P<questid>.+)$', views.data_get, name='api_get'),
  url(r'^do$', views.data_do, name='api_do'),
  url(r'^$', views.mainpage, name='action_home'),
)
