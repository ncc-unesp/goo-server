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

from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase, TestApiClient
from core.models import *

class AuthResourceTest(ResourceTestCase):
    fixtures = ['test_auth.json']

    def setUp(self):
        super(AuthResourceTest, self).setUp()

        self.client = TestApiClient()

        self.endpoint = '/api/v1/auth/'
        self.format = 'json'

        # Get user 1 and token 1 from fixture
        self.user = User.objects.all()[0]
        self.token = self.user.usertoken_set.all()[0]

        self.password = '123'
        self.detail = '/api/v1/auth/{0}/'.format(self.token.id)

        # Get user 2 and token 2 from fixture
        self.user2 = User.objects.all()[1]
        self.token2 = self.user2.usertoken_set.all()[0]

        self.detail2 = '/api/v1/auth/{0}/'.format(self.token2.id)

    def get_credentials(self):
        return self.create_basic(username=self.user.username,
                                 password=self.password)

    # Try to get tokens without credentials
    def test_get_keys_unauthorzied(self):
        self.assertHttpUnauthorized(self.client.get(self.endpoint,
                                    self.format))

    # Try to create a token (POST)
    def test_create_token_json(self):
        post_data = {}
        credentials = self.get_credentials()
        self.assertHttpCreated(self.client.post(self.endpoint,
                                                    self.format,
                                                    data=post_data,
                                                    authentication=credentials))
    # Try to get all tokens (GET)
    def test_get_keys_json(self):
        credentials = self.get_credentials()
        resp = self.client.get(self.endpoint,
                                   self.format,
                                   authentication=credentials)
        self.assertValidJSONResponse(resp)

    # Try to delete a token (DELETE)
    def test_delete_token_json(self):
        credentials = self.get_credentials()
        self.assertEqual(UserToken.objects.count(), 2)
        resp = self.client.delete(self.detail,
                                      format=self.format,
                                      authentication=credentials)
        self.assertHttpAccepted(resp)
        self.assertEqual(UserToken.objects.count(), 1)

    # User 1 try to delete user 2 token
    def test_delete_another_token(self):
        credentials = self.get_credentials()
        self.assertHttpNotFound(self.client.delete(self.detail2,
                                format=self.format,
                                authentication=credentials))

    # Try to create a token (POST) with wrong credentials
    def test_create_token_with_wrong_credentials_json(self):
        post_data = {}
        credentials = self.create_basic(username=self.user.username,
                                        password="bla")
        self.assertHttpUnauthorized(self.client.post(self.endpoint,
                                                     self.format,
                                                     data=post_data,
                                                     authentication=credentials))


class CheckTokenTest(ResourceTestCase):
    def setUp(self):
        super(CheckTokenTest, self).setUp()

        self.client = TestApiClient()

        self.endpoint = '/api/v1/token/'
        self.format = 'json'

        # Create one user
        self.user = User(username="testuser")
        self.user.save()

        # Create on token
        self.token = UserToken(user=self.user)
        self.token.save()

    # check for the token ttl
    def test_check_token(self):
        url = "%s?token=%s" % (self.endpoint, self.token.token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

    # check for the WRONG token ttl
    def test_check_wrong_token(self):
        url = "%s?token=%s" % (self.endpoint, "not-a-valid-token")
        self.assertHttpUnauthorized(self.client.get(url, self.format))

    # check for the NO token ttl
    def test_check_no_token(self):
        self.assertHttpUnauthorized(self.client.get(self.endpoint, self.format))

class ApplicationTest(ResourceTestCase):
    def setUp(self):
        super(ApplicationTest, self).setUp()

        self.client = TestApiClient()

        self.endpoint = '/api/v1/apps/'
        self.format = 'json'

        # Create one user
        self.user = User(username="testuser")
        self.user.save()

        # Create on token
        self.token = UserToken(user=self.user)
        self.token.save()

    # list apps
    def test_get_apps(self):
        url = "%s?token=%s" % (self.endpoint, self.token.token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

    # list apps details
    def test_get_apps_details(self):
        app_id = Application.objects.all()[0].id
        url = "%s%d/?token=%s" % (self.endpoint, app_id, self.token.token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

class JobTest(ResourceTestCase):
    def setUp(self):
        super(JobTest, self).setUp()

        self.client = TestApiClient()

        self.endpoint = '/api/v1/jobs/'
        self.format = 'json'

        # Create one user
        self.user = User(username="testuser")
        self.user.save()

        # Create on token
        self.token = UserToken(user=self.user)
        self.token.save()

        # create a job
        self.job = Job(user=self.user, application=Application.objects.all()[0])
        self.job.save()

    def test_get_job_list(self):
        url = "%s?token=%s" % (self.endpoint, self.token.token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

    def test_get_job_detail(self):
        url = "%s%d/?token=%s" % (self.endpoint, self.job.id, self.token.token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

    def test_post_job(self):
        data = {"application" : "/api/v1/apps/1/"}
        url = "%s?token=%s" % (self.endpoint, self.token.token)
        self.assertHttpCreated(self.client.post(url, self.format, data=data))

    def test_patch_job(self):
        job = Job(user=self.user, application=Application.objects.all()[0])
        job.save()
        data = {"progress":"50"}
        url = "%s%d/?token=%s" % (self.endpoint, job.id, self.token.token)
        resp = self.client.patch(url, self.format, data=data)
        self.assertHttpAccepted(resp)

    def test_delete_job(self):
        job = Job(user=self.user, application=Application.objects.all()[0])
        job.save()
        url = "%s%d/?token=%s" % (self.endpoint, job.id, self.token.token)
        self.assertHttpAccepted(self.client.delete(url, self.format))
