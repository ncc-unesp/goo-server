# This file is part of goo-server.
#
# Copyright (c) 2103-2014 by Núcleo de Computação Científica, UNESP
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
from dispatcher.models import Pilot
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class PilotTokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        try:
            token = request.REQUEST['token']
        except KeyError:
            return False

        try:
            # query DB for token and return pilot
            pilot = Pilot.objects.filter(token=token).get()
        except Pilot.DoesNotExist, Pilot.MultipleObjectsReturned:
            # error - no token (or more than one)
            return False

        if pilot:
            request.pilot = pilot

            # try to save user of the current job, when available
            # this allow the pilot to PATCH with the objs (m2m) info.
            job = pilot.get_current_job()
            if job:
                request.user = job.user

            return True

        return False # pragma: no cover

class PilotAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(pilot=bundle.request.pilot)

    def read_detail(self, object_list, bundle):
        return bundle.obj.pilot == bundle.request.pilot

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.pilot == bundle.request.pilot

    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.pilot == bundle.request.pilot:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.pilot == bundle.request.pilot

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
