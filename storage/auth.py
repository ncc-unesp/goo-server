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
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from core.models import UserToken
from dispatcher.models import Pilot

from storage.models import DataProxyServer as DPS

from django.utils.timezone import now

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

from django.db.models import Q

class StorageAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        try:
            user_token = request.REQUEST['token']
        except KeyError:
            return False

        # try to find server (DPS) id by token
        try:
            # query DB for servers whith this token
            server_token = request.REQUEST['proxy_token']
            request.dps = DPS.objects.filter(enabled=True)
            request.dps = request.dps.get(token=server_token)
        except (KeyError, DPS.DoesNotExist, DPS.MultipleObjectsReturned):
            # direct request, no DPS token
            request.dps = None

        # lets try user tokens first
        try:
            # query DB for token and return user
            t = UserToken.objects.filter(expire_time__gt=now())
            user = t.get(token=user_token).user
        except (UserToken.DoesNotExist, UserToken.MultipleObjectsReturned):
            # now, lets try pilot tokens
            try:
                # query DB for token and return pilot
                pilot = Pilot.objects.filter(token=user_token).get()

                job = pilot.get_current_job()
                if not job:
                    return False
                else:
                    user = job.user

            except Pilot.DoesNotExist, Pilot.MultipleObjectsReturned:
                # error - no token (or more than one)
                return False

        if user:
            request.user = user
            return True

        return False # pragma: no cover

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class StorageAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(Q(user=bundle.request.user) | Q(public=True))

    def read_detail(self, object_list, bundle):
        return (bundle.obj.user == bundle.request.user) | bundle.obj.public

    def create_list(self, object_list, bundle):
        # only allow creation from a DPS request
        if not bundle.request.dps:
            return Unauthorized
        return object_list

    def create_detail(self, object_list, bundle):
        if not bundle.request.dps:
            return Unauthorized
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        return Unauthorized

    def update_detail(self, object_list, bundle):
        return Unauthorized

    def delete_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
