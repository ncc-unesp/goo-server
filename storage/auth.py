# vim: tabstop=4 shiftwidth=4 softtabstop=4

from core.models import UserToken
from dispatcher.models import Pilot

from django.utils.timezone import now

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

class AnyTokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        try:
            token = request.REQUEST['token']
        except KeyError:
            return False

        # lets try user tokens first
        try:
            # query DB for token and return user
            t = UserToken.objects.filter(expire_time__gt=now())
            user = t.get(token=token).user
        except UserToken.DoesNotExist, UserToken.MultipleObjectsReturned:
            # now, lets try pilot tokens
            try:
                # query DB for token and return pilot
                pilot = Pilot.objects.filter(token=token).get()

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
