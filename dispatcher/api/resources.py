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
from tastypie.resources import ModelResource
from dispatcher.auth import PilotTokenAuthentication, PilotAuthorization

from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import NotFound
from tastypie import fields

from dispatcher.models import Pilot
from core.models import Job
from core.api.resources import ApplicationResource
from storage.api.resources import DataObjectResource

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

    def get_object_list(self, request):
        ol = super(CheckPilotTokenResource, self).get_object_list(request)
        return ol.filter(token=request.REQUEST['token'])

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

    input_objs = fields.ToManyField(DataObjectResource, 'input_objs', null=True, full=True)
    output_objs = fields.ToManyField(DataObjectResource, 'output_objs', null=True, full=True)
    checkpoint_objs = fields.ToManyField(DataObjectResource, 'checkpoint_objs', null=True, full=True)

    class Meta:
        resource_name = 'dispatcher'
        authentication = PilotTokenAuthentication()
        authorization = PilotAuthorization()
        # Remove from query deleted jobs
        queryset = Job.objects.all()
        list_allowed_methods = ['post']
        detail_allowed_methods = ['get', 'patch']
        # Return data on the POST query
        always_return_data = True

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
