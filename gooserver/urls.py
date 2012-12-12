# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf.urls import patterns, include, url
from tastypie.api import Api
from core.api.resources import *
from dispatcher.api.resources import *
from storage.api.resources import *

v1_api = Api(api_name='v1')
v1_api.register(ApplicationResource())
v1_api.register(JobResource())
v1_api.register(AuthResource())
v1_api.register(PilotJobResource())
v1_api.register(DataProxyServerResource())

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gooserver.views.home', name='home'),
    # url(r'^gooserver/', include('gooserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)
