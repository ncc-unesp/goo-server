# vim: tabstop=4 shiftwidth=4 softtabstop=4

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from storage.auth import StorageAuthentication, StorageAuthorization
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
        authentication = StorageAuthentication()
        authorization = Authorization()
        # Remove token from any query
        excludes = ['token']
        # Remove from query disabled data proxy servers
        queryset = DataProxyServer.objects.filter(~Q(enabled = False))
        list_allowed_methods = ['get',]
        detail_allowed_methods = []

class DataObjectResource(ModelResource):
    """This resource handler objects requests.

    Allowed Methods:
    ----------------

        GET    /dataobjects/             # Get all objects of an user
        GET    /dataobjects/{id}         # Get info about an user object
        POST   /dataobjects/             # Submmit a new object
        DELETE /dataobjects/{id}/        # Delete a object
    """

    data_proxy_servers = fields.ToManyField(DataProxyServerResource,
                                            'data_proxy_servers',
                                            null=True, full=True)

    class Meta:
        resource_name = 'dataobjects'
        authentication = StorageAuthentication()
        authorization = StorageAuthorization()
        queryset = DataObject.objects.all()
        list_allowed_methods = ['get', 'post', ]
        detail_allowed_methods = ['get', 'delete', ]

        # Return data on the POST query
        always_return_data = True

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(Q(user=request.user) | Q(public=True))

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return super(DataObjectResource, self).hydrate(bundle)

    def hydrate_m2m(self, bundle):
        bundle.obj.data_proxy_servers.add(bundle.request.dps)
        return super(DataObjectResource, self).hydrate_m2m(bundle)
