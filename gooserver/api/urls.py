from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import ApplicationHandler
from api import views
from piston.doc import documentation_view

application_handler = Resource(ApplicationHandler)

urlpatterns = patterns('',
   url(r'^doc/', documentation_view),

   url(r'^app/(?P<app_id>[^/]+)/', application_handler),
   url(r'^apps/', application_handler),
)
