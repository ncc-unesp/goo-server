# vim: tabstop=4 shiftwidth=4 softtabstop=4

from tastypie.resources import ModelResource, Resource
from tastypie import fields
from django.db.models import Q
from core.models import *

from storage.api.resources import ObjectResource

from core.auth import UserTokenAuthentication
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization

from django.utils.timezone import now

from django.conf.urls import url
from tastypie.utils import trailing_slash

class AuthResource(ModelResource):
    """This resource handler auth requests.

    Allowed Methods:
    ----------------

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
    ----------------

        GET    /check_token/          # Return token ttl

    """
    class Meta:
        resource_name = 'check_token'
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
    ----------------

        GET    /apps/                # Get all apps on grid
        GET    /apps/{id}            # Get info about a app
        GET    /apps/schema/         # Get app schema
        GET    /apps/set/{id};{id}/  # Get a list of apps
    """

    app_obj = fields.ForeignKey(ObjectResource, 'app_obj', null=True)

    class Meta:
        resource_name = 'apps'
        authentication = UserTokenAuthentication()
        authorization = ReadOnlyAuthorization()
        queryset = Type.objects.all()
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        list_exclude = ['executable', 'app_obj', 'args', 'inputs',
                        'outputs', 'checkpoints', 'shared_fs',]


    def dehydrate_name(self, bundle):
        return bundle.obj

    def dehydrate(self, bundle):
        if self.get_resource_uri(bundle) != bundle.request.path:
            list_exclude = self._meta.list_exclude
            for item in list_exclude:
                del bundle.data[item]
        return bundle

#    def dehydrate(self, bundle):
#        bundle.data['custom_field'] = "Whatever you want"
#        return bundle

class JobResource(ModelResource):
    """This resource handler jobs requests.

    Allowed Methods:
    ----------------

        GET    /jobs/                # Get all jobs of an user
        GET    /jobs/{id}            # Get info about an user job
        GET    /jobs/schema/         # Get job schema
        GET    /jobs/set/{id};{id}/  # Get a list of jobs
        POST   /jobs/                # Submmit a new job
        PATCH  /jobs/{id}/           # Partially update a job
        DELETE /jobs/{id}/           # Delete a job
    """

    type = fields.ForeignKey(ApplicationResource, 'type')

    class Meta:
        resource_name = 'jobs'
        authentication = UserTokenAuthentication()
        authorization = Authorization()
        # Remove from query deleted jobs
        queryset = Job.objects.filter(~Q(status = 'D'))
        list_allowed_methods = ['get', 'post', ]
        detail_allowed_methods = ['get', 'patch', 'delete', ]
        list_exclude = ['return_code', 'hosts', 'eta', 'input_obj_id',
                        'output_obj_id', 'memory_in_use', 'memory_requirement',
                        'start_time', 'restart', 'ttl', 'pph',
                        'checkpoing_obj_id', 'disk_requirement', 'disk_in_use',
                        'create_time', 'end_time', 'modification_time', ]

        # Return data on the POST query
        always_return_data = True


    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

#    def dehydrate(self, bundle):
#        if self.get_resource_uri(bundle) != bundle.request.path:
#            list_exclude = self._meta.list_exclude
#            for item in list_exclude:
#                del bundle.data[item]
#        return bundle

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        bundle.obj.type_id = int(bundle.data['app_id'])
        return bundle
