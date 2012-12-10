from tastypie.resources import ModelResource
from dispatcher.auth import PilotTokenAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound

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
        # Return data on the POST query
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(pilot=request.pilot)

    def obj_create(self, bundle, **kwargs):
        time_left = bundle.request.REQUEST.get('time_left', None)
        if not time_left:
            # missing mandatory param time_left (in seconds)
            raise LookupError
        else:
            time_left = int(time_left)

        try:
            bundle.obj = bundle.request.pilot.get_new_job(time_left)
        except StopIteration:
            # no jobs found
            raise NotFound("No jobs found")

        return bundle
