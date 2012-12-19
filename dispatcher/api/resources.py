from tastypie.resources import ModelResource
from dispatcher.auth import PilotTokenAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie import fields

from core.models import Job
from core.api.resources import ApplicationResource
from storage.api.resources import ObjectResource

from django.template.defaultfilters import slugify

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

    app = fields.ToOneField(ApplicationResource, 'type', null=True)

    input_objs = fields.ToManyField(ObjectResource, 'input_objs', null=True)
    output_objs = fields.ToManyField(ObjectResource, 'output_objs', null=True)
    checkpoint_objs = fields.ToManyField(ObjectResource, 'checkpoint_objs', null=True)

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

    def dehydrate(self, bundle):
        bundle.data['slug'] = slugify(bundle.obj.name)

    def obj_create(self, bundle, **kwargs):
        try:
            time_left = int(bundle.data['time_left'])
        except KeyError, ValueError:
            # missing mandatory param time_left (in seconds)
            # or not a int
            raise NotFound("No time_left argument")

        try:
            bundle.obj = bundle.request.pilot.get_new_job(time_left)
        except StopIteration:
            # no jobs found
            raise NotFound("No jobs found")

        return bundle
