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
from tastypie.test import ResourceTestCase, TestApiClient
from dispatcher.models import *
from core.models import *

class PilotJobResourceTest(ResourceTestCase):
    fixtures = ['local_site.json']

    def setUp(self):
        super(PilotJobResourceTest, self).setUp()

        self.client = TestApiClient()

        self.endpoint = '/api/v1/dispatcher/'
        self.format = 'json'

        # Create one user
        self.user = User(username="testuser")
        self.user.save()

        # create a job
        self.job = Job(user=self.user, application=Application.objects.all()[0])
        self.job.maxtime = 30
        self.job.save()

        self.site = Site.objects.get(pk=1)
        self.pilot = self.site.submit_pilot_based_on_job(self.job)

    def test_submit_pilot(self):
        pilot = self.site.submit_pilot_based_on_job(self.job)
        self.assertEqual(type(pilot), type(Pilot()))

    def test_pilot_post_job(self):
        self.job.status='P'
        self.job.save()

        data = {"time_left": 60}
        token = self.pilot.token
        url = "%s?token=%s" % (self.endpoint, token)
        request = self.client.post(url, self.format, data=data)
        self.assertHttpCreated(request)

    def test_pilot_get_job(self):
        self.job.status='R'
        self.job.pilot = self.pilot
        self.job.save()

        token = self.pilot.token
        url = "%s%d/?token=%s" % (self.endpoint, self.job.id, token)
        request = self.client.get(url, self.format)
        self.assertValidJSONResponse(request)

    def test_wrong_token(self):
        url = "%s%d/?token=%s" % (self.endpoint, self.job.id, "not-a-valid-token")
        request = self.client.get(url, self.format)
        self.assertHttpUnauthorized(request)

    def test_no_token(self):
        url = "%s%d/" % (self.endpoint, self.job.id)
        request = self.client.get(url, self.format)
        self.assertHttpUnauthorized(request)

    def test_pilot_patch_job(self):
        self.job.status='R'
        self.job.pilot = self.pilot
        self.job.save()

        data = {"progress": 50}
        token = self.pilot.token
        url = "%s%d/?token=%s" % (self.endpoint, self.job.id, token)
        request = self.client.patch(url, self.format, data=data)
        self.assertHttpAccepted(request)
