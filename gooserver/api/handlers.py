from piston.handler import BaseHandler
from core.models import *
from piston.doc import generate_doc
from django.contrib.auth.decorators import login_required
from api.decorators import *

class AuthHandler(BaseHandler):
    """This handler is responsible for performing authentication with the web
    service.
    """
    allowed_methods = ('POST',)
    model = UserToken

    @staticmethod
    def resource_uri():
        return('token', [])

    def create(self, request):
        """Get a new authentication token. This is the first and most important
        method to be executed. You will need for all other request a token, and
        this method give to you this token.

        **Note:** A token has an expire date.

        Basic HTTP Authentication:
        --------------------------

        user: (required)
            Your username
        password: (required)
            Your password

        Request:
        --------
        ::

            $ curl -u username:password -X POST https://goo.ncc.unesp.br/api/v1/auth/get_token/

        Return:
        -------
        ::

            {
                "token": "18e2f86f-9a10-4cc4-a6aa-6a201ff2c558",
                "owner": "username",
                "expires": "2010-11-01T03:32:15-05:00",
            }
        """
        user = request.user
        token = UserToken(user=user)
        token.save()
        data = { "token"  : token.token,
                 "owner"  : user.username,
                 "expires": token.expire_time }
        return data

class AppsHandler(BaseHandler):
    """With this handler you can get informations about the NCC grid pre
    installed applications. You will need of one application to submit a job to
    the grid.
    """

    @staticmethod
    def resource_uri():
        return('apps', [])

    @check_token
    def read(self, request):
        """Get a list of all pre installed applications on NCC grid.

        Arguments:
        ----------

        token: (required)
            Your API auth token

        Request:
        --------
        ::

            $ curl -X GET https://goo.ncc.unesp.br/api/v1/apps/?token=18e2f86f-9a10-4cc4-a6aa-6a201ff2c558

        Return:
        -------
        ::

            [
                {
                    "app": "BEAST Serial",
                    "version": "1.6.1",
                    "id": 1
                },
                {
                    "app": "BEAST SMP",
                    "version": "1.6.1",
                    "id": 2
                },
                {
                    "app": "Clustalw MPI",
                    "version": "1.82",
                    "id": 3
                }
            ]
        """

        types = Type.objects.all()
        data = []
        for type in types:
            data.append({'id': type.id, 'app': "%s %s" % (type.version.application.name,
                                                          type.name),
                         'version': type.version.version})
        return data

class JobsHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE',)
    model = Job

    @staticmethod
    def resource_uri():
        return('jobs', [])

    @check_token
    def read(self, request):
        """List all jobs of an user.

        Arguments:
        ----------

        token: (required)
            Your API auth token


        Request:
        --------
        ::

            $ curl -X GET https://goo.ncc.unesp.br/api/v1/jobs/?token=18e2f86f-9a10-4cc4-a6aa-6a201ff2c558

        Return:
        -------
        ::

            [
                {
                    "app": "BEAST Serial",
                    "version": "1.6.1",
                    "id": 1
                },
                {
                    "app": "BEAST SMP",
                    "version": "1.6.1",
                    "id": 2
                },
                {
                    "app": "Clustalw MPI",
                    "version": "1.82",
                    "id": 3
                }
            ]

        """
        user = request.user
        data = []
        jobs = user.get_jobs()
#        for job in jobs:
#            data.append({'id': job.id,
#                         'name': job.name,
#                         'priority': job.priority,
#                         'status': job.status,
#                         'return_code': job.return_code})
        return data

    @check_token
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

    @check_token
    def delete(self, request):
        """Delete a job from the system.

        Arguments:
        ----------

        token: `(required)`
            Your API auth token
        """
        return None

    @check_token
    def update(self, request):
        """Update job informations or state.

        Arguments:
        ----------

        token: `(required)`
            Your API auth token
        action
            What action do you want to execute. Default is `no action`.

        Supported actions:
        ------------------

        cancel:
            Cancel a job
        """
        return None
