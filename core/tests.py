# vim: tabstop=4 shiftwidth=4 softtabstop=4

import datetime
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

    def get_token(self):
        return self.token.token

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

        self.endpoint = '/api/v1/check_token/'
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
    def test_check_token(self):
        url = "%s?token=%s" % (self.endpoint, "not-a-valid-token")
        self.assertHttpUnauthorized(self.client.get(url, self.format))

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
        app_id = Version.objects.all()[0].id
        url = "%s%d/?token=%s" % (self.endpoint, app_id, self.token.token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

#GET jobs
#GET jobs/{id}
#POST jobs
#PATCH jobs/{id}
#DELETE jobs/{id}
