# This file is part of goo-server.
#
# Copyright (c) 2103-2014 by Nucleo de Computacao Cientifica, UNESP
#
# Authors:
#    Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#    Gabriel von. Winckler <winckler AT ncc DOT unesp DOT br>
#
# goo-server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# goo-server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
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

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return super(DataObjectResource, self).hydrate(bundle)

    def hydrate_m2m(self, bundle):
        bundle.obj.data_proxy_servers.add(bundle.request.dps)
        return super(DataObjectResource, self).hydrate_m2m(bundle)
