from dispatcher.models import Pilot
from tastypie.authentication import Authentication

class PilotTokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        if not request.REQUEST['token']:
            return False
        token = request.REQUEST['token']

        try:
            # query DB for token and return pilot
            pilot = Pilot.objects.filter(token=token).get()
        except Pilot.DoesNotExist, Pilot.MultipleObjectsReturned:
            # error - no token (or more than one)
            return False

        if pilot:
            request.pilot = pilot
            return True

        return False
