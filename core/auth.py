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

from django.conf import settings
from django.contrib.auth.models import User, check_password
from core.models import UserToken

from django.utils.timezone import now

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

from django.db.models import Q

class UserTokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        try:
            token = request.REQUEST['token']
        except KeyError:
            return False

        try:
            # query DB for token and return user
            t = UserToken.objects.filter(expire_time__gt=now())
            user = t.get(token=token).user
        except UserToken.DoesNotExist, UserToken.MultipleObjectsReturned:
            # error - no token (or more than one)
            return False

        if user:
            request.user = user
            return True

        return False # pragma: no cover

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

class ApplicationAuthorization(UserObjectsOnlyAuthorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(Q(_public=True)|Q(_user=bundle.request.user))

    def read_detail(self, object_list, bundle):
        return (bundle.obj._user == bundle.request.user) | bundle.obj._public

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj._user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj._user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj._user == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
