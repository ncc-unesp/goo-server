# vim: tabstop=4 shiftwidth=4 softtabstop=4

from core.models import UserToken
from dispatcher.models import Pilot

from storage.models import DataProxyServer as DPS

from django.utils.timezone import now

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class StorageAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        try:
            server_token = request.REQUEST['proxy_token']
            user_token = request.REQUEST['token']
        except KeyError:
            return False

        # try to find server (DPS) id by token
        try:
            # query DB for servers whith this token
            request.dps = DPS.objects.filter(enabled=True)
            request.dps = request.dps.get(token=server_token)
        except DPS.DoesNotExist, DPS.MultipleObjectsReturned:
            # direct request, no DPS token
            request.dps = None

        # lets try user tokens first
        try:
            # query DB for token and return user
            t = UserToken.objects.filter(expire_time__gt=now())
            user = t.get(token=user_token).user
        except UserToken.DoesNotExist, UserToken.MultipleObjectsReturned:
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
    def create_list(self, object_list, bundle):
        if not bundle.request.dps:
            return Unauthorized

        return object_list
