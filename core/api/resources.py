# vim: tabstop=4 shiftwidth=4 softtabstop=4

from tastypie.resources import ModelResource, Resource
from tastypie import fields
from django.db.models import Q
from core.models import *

from storage.api.resources import ObjectResource

from core.auth import UserTokenAuthentication
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization

from django.utils.timezone import now
from django.template.defaultfilters import slugify

from django.conf.urls import url
from tastypie.utils import trailing_slash

class AuthResource(ModelResource):
    """This resource handler auth requests.

    Allowed Methods:

        GET    /auth/                # Get all tokens of an user
        GET    /auth/{id}            # Get info about an user token
        GET    /auth/schema/         # Get auth schema
        GET    /auth/set/{id};{id}/  # Get a list of tokens

        POST   /auth/                # Ask for a new token
        DELETE /auth/                # Revoke all tokens of an user.
        DELETE /auth/{id}            # Revoke an user token.

    """
    class Meta:
        resource_name = 'auth'
        authentication = BasicAuthentication()
        authorization = Authorization()
        allowed_methods = ['get','post', 'delete']
        fields = ['token', 'expire_time']
        # only select valid tokens (not expired)
        queryset = UserToken.objects.filter(expire_time__gt=now())
        # return token on POST request
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

class CheckTokenResource(ModelResource):
    """This resource handler auth token requests.

    Allowed Methods:

        GET    /token/          # Return token ttl if is valid

    """
    class Meta:
        resource_name = 'token'
        authentication = UserTokenAuthentication()
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = []
        detail_allowed_methods = ['get']
        fields = ['expire_time']
        include_resource_uri = False
        # only select valid tokens (not expired)
        queryset = UserToken.objects.filter(expire_time__gt=now())

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name,
                                                trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail'),
        ]

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(token=request.REQUEST['token'])


class ApplicationResource(ModelResource):
    """This resource handler app requests.

    Allowed Methods:

        GET    /apps/                # Get all apps on grid
        GET    /apps/{id}            # Get info about a app
        GET    /apps/schema/         # Get app schema
        GET    /apps/set/{id};{id}/  # Get a list of apps
    """

    _app_obj = fields.ToOneField(ObjectResource, '_app_obj', null=True)

    class Meta:
        resource_name = 'apps'
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
        queryset = Application.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle.data['_name'] = str(bundle.obj)
        return bundle


class JobResource(ModelResource):
    """This resource handler jobs requests.

    Allowed Methods:

        GET    /jobs/                # Get all jobs of an user
        GET    /jobs/{id}            # Get info about an user job
        GET    /jobs/schema/         # Get job schema
        GET    /jobs/set/{id};{id}/  # Get a list of jobs
        POST   /jobs/                # Submmit a new job
        PATCH  /jobs/{id}/           # Partially update a job
        DELETE /jobs/{id}/           # Delete a job
    """

    application = fields.ToOneField(ApplicationResource, 'application')

    input_objs = fields.ToManyField(ObjectResource, 'input_objs', null=True, full=True)
    output_objs = fields.ToManyField(ObjectResource, 'output_objs', null=True, full=True)
    checkpoint_objs = fields.ToManyField(ObjectResource, 'checkpoint_objs', null=True, full=True)

    class Meta:
        resource_name = 'jobs'
        authentication = UserTokenAuthentication()
        authorization = Authorization()
        # Remove from query deleted jobs
        queryset = Job.objects.filter(~Q(status = 'D'))
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'patch', 'delete']
        list_exclude = ['return_code', 'hosts', 'eta', 'memory_in_use',
                        'memory', 'start_time', 'restart',
                        'maxtime', 'cores_per_host', 'diskspace', 'diskspace_in_use',
                        'create_time', 'end_time', 'modification_time',
                        'input_objs', 'output_objs', 'checkpoint_objs']

        # Return data on the POST query
        always_return_data = True


    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def dehydrate(self, bundle):
        if self.get_resource_uri(bundle) != bundle.request.path:
            # list request
            list_exclude = self._meta.list_exclude
            for item in list_exclude:
                del bundle.data[item]
        else:
            # detail request
            bundle.data['slug'] = slugify(bundle.obj.name)
        bundle.data['app_name'] = bundle.obj.application

        return bundle

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle
