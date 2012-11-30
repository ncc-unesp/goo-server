from piston.handler import BaseHandler
from core.models import *
from piston.doc import generate_doc
from django.contrib.auth.decorators import login_required
from api.decorators import *

class AuthTokenHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = UserToken

    @staticmethod
    def resource_uri():
        return('token', [])

    # TODO: Double check authentication (winckler)
    def create(self, request):
        """Get a new authentication token.

        Basic HTTP Authentication:
        --------------------------

        user: `(required)`
            Your username
        password: `(required)`
            Your password

        Return Example:
        ---------------
        ::

            {
                "token": "18e2f86f-9a10-4cc4-a6aa-6a201ff2c558"
            }
        """
        user = request.user
        token = UserToken(user=user)
        token.save()
        data = { "token": token.token }
        return data

class JobsHandler(BaseHandler):
    allowed_methods = ('GET', 'POST',)
    model = Job

    @staticmethod
    def resource_uri():
        return('jobs', [])

    @check_token
    def read(self, request):
        """List all jobs of an user.

        Arguments:
        ----------

        token: `(required)`
            Your API auth token

        """
        print "Executing read"
        data = {"msg":"Hello world"}
        return data

    def create(self, request):
        """Submmit a job to the system.

        Arguments:
        ----------

        token: `(required)`
            Your API auth token
        name
            Your job name
        type
            Application type
        """
        print "Executing create"
        data = {"msg":"Hello world"}
        return data

class JobsIdHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Job

    @staticmethod
    def resource_uri():
        return('jobs_id', ['job_id'])

    def read(self, request):
        """Get job information.

        Arguments:
        ----------

        token: `(required)`
             Your API auth token
        content
            Content type to retrieve (`status` or `log`). \
            Default is `status`.
        """

        print "Executing info"
        return None

    def delete(self, request):
        """Delete a job from the system.

        Arguments:
        ----------

        token: `(required)`
            Your API auth token
        """
        return None

    def update(self, request):
        """Update job informations or state.

        Arguments:

        token: `(required)`
            Your API auth token
        action
            What action do you want to execute. Default is `no action`.

        Supported actions:
        ------------------

        :cancel: Cancel a job
        """
        return None
