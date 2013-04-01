from tastypie.resources import ModelResource
from dispatcher.auth import PilotTokenAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.exceptions import NotFound
from tastypie import fields

from dispatcher.models import Pilot
from core.models import Job
from core.api.resources import ApplicationResource
from storage.api.resources import ObjectResource

from django.template.defaultfilters import slugify
from django.conf.urls import url
from tastypie.utils import trailing_slash

class CheckPilotTokenResource(ModelResource):
    """This resource handler auth token requests.

    Allowed Methods:

        GET    /pilot/token/          # Return if pilot token is valid

    """
    class Meta:
        resource_name = 'pilot/token'
        authentication = PilotTokenAuthentication()
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        fields = ['token']
        include_resource_uri = False
        # only select valid tokens (not expired)
        queryset = Pilot.objects.all()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name,
                                                trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail'),
        ]

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(token=request.REQUEST['token'])

    def dehydrate(self, bundle):
        bundle.data['valid'] = True
        return bundle

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

    application = fields.ToOneField(ApplicationResource, 'application', full=True)

    input_objs = fields.ToManyField(ObjectResource, 'input_objs', null=True, full=True)
    output_objs = fields.ToManyField(ObjectResource, 'output_objs', null=True, full=True)
    checkpoint_objs = fields.ToManyField(ObjectResource, 'checkpoint_objs', null=True, full=True)

    class Meta:
        resource_name = 'dispatcher'
        authentication = PilotTokenAuthentication()
        authorization = Authorization()
        # Remove from query deleted jobs
        queryset = Job.objects.all()
        list_allowed_methods = ['post']
        detail_allowed_methods = ['get', 'patch']
        # Return data on the POST query
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(pilot=request.pilot)

    def dehydrate(self, bundle):
        bundle.data['slug'] = slugify(bundle.obj.name)
        return bundle

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
