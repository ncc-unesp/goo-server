# vim: tabstop=4 shiftwidth=4 softtabstop=4

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from storage.auth import AnyTokenAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from django.db.models import Q
from storage.models import *
from datetime import datetime

class DataProxyServerResource(ModelResource):
    """This resource handler DataProxyServers.

    Allowed Methods:
    ----------------

        GET    /dataproxyserver/    # Get all Data Proxy Servers (DPS)
    """

    class Meta:
        resource_name = 'dataproxyserver'
        authentication = AnyTokenAuthentication()
        authorization = Authorization()
        # Remove from query disabled data proxy servers
        queryset = DataProxyServer.objects.filter(~Q(enabled = False))
        list_allowed_methods = ['get',]
        detail_allowed_methods = []

class ObjectResource(ModelResource):
    """This resource handler objects requests.

    Allowed Methods:
    ----------------

        GET    /objects/             # Get all objects of an user
        GET    /objects/{id}         # Get info about an user object
        POST   /objects/             # Submmit a new object
        DELETE /objects/{id}/        # Delete a object
    """
    class Meta:
        resource_name = 'objects'
        authentication = AnyTokenAuthentication()
        authorization = Authorization()
        queryset = Object.objects.all()
        list_allowed_methods = ['get', 'post', ]
        detail_allowed_methods = ['get', 'delete', ]

        # Return data on the POST query
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(user=request.user) | Q(public=True))

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle
