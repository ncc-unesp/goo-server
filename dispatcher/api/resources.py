from tastypie.resources import ModelResource
from dispatcher.auth import PilotTokenAuthentication
from tastypie.authorization import Authorization

from core.models import Job

class PilotJobResource(ModelResource):
    """This resource handler jobs requests.

    Allowed Methods:
    ----------------

        GET    /dispatcher/{id}            # Get info about an job
        GET    /dispatcher/schema/         # Get job schema
        GET    /dispatcher/set/{id};{id}/  # Get a list of jobs
        POST   /dispatcher/                # Get a new job
        PATCH  /dispatcher/{id}/           # Partially update a job
    """

    class Meta:
        resource_name = 'dispatcher'
        authentication = PilotTokenAuthentication()
        authorization = Authorization()
        # Remove from query deleted jobs
        queryset = Job.objects.all()
        #list_allowed_methods = ['post']
        list_allowed_methods = ['post', 'get']
        detail_allowed_methods = ['get', 'patch']

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(pilot=request.pilot)
