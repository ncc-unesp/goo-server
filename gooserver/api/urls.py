from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import *
from api import views
from piston.doc import documentation_view
from api.authentication import NCCAuthentication

auth = NCCAuthentication(realm="NCC Auth")

# Token handlers
token = Resource(AuthHandler, authentication=auth)

# Applications handlers
apps = Resource(AppsHandler)

# Jobs handlers
jobs = Resource(JobsHandler)

urlpatterns = patterns('',
   url(r'^doc/', documentation_view),

   url(r'^auth/get_token/', token, name="token"),

   url(r'^apps/', apps, name="apps"),

   url(r'^jobs/', jobs, name="jobs"),
   url(r'^jobs/(?P<job_id>[^/]+)/', jobs, name="job_info"),
)
