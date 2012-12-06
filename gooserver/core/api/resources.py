from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from core.authentication import UserTokenAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from django.db.models import Q
from core.models import *
from datetime import datetime

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
        queryset = UserToken.objects.filter(expire_time__gt=datetime.now())
        # return token on POST request
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle


class ApplicationResource(ModelResource):
    """This resource handler app requests.

    Allowed Methods:
    ----------------

        GET    /apps/                # Get all apps on grid
        GET    /apps/{id}            # Get info about a app
        GET    /apps/schema/         # Get app schema
        GET    /apps/set/{id};{id}/  # Get a list of apps
    """
    class Meta:
        resource_name = 'apps'
        authentication = UserTokenAuthentication()
        authorization = ReadOnlyAuthorization()
        queryset = Type.objects.all()
        fields = ['id', 'name', 'multi_hosts', 'multi_thread',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]

    def dehydrate_name(self, bundle):
        return bundle.obj

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
        PUT    /jobs/{id}/           # Update a job
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
        detail_allowed_methods = ['get', 'put', 'patch', 'delete', ]
        list_exclude = ['return_code', 'hosts', 'eta', 'input_obj_id',
                        'output_obj_id', 'memory_in_use', 'memory_requirement',
                        'start_time', 'restart', 'ttl', 'pph',
                        'checkpoing_obj_id', 'disk_requirement', 'disk_in_use',
                        'create_time', 'end_time', 'modification_time', ]

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def dehydrate(self, bundle):
        if self.get_resource_uri(bundle) != bundle.request.path:
            list_exclude = self._meta.list_exclude
            for item in list_exclude:
                del bundle.data[item]
        return bundle

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle
