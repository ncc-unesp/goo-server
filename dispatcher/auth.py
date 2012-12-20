from dispatcher.models import Pilot
from tastypie.authentication import Authentication

class PilotTokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        try:
            token = request.REQUEST['token']
        except KeyError:
            return False

        try:
            # query DB for token and return pilot
            pilot = Pilot.objects.filter(token=token).get()
        except Pilot.DoesNotExist, Pilot.MultipleObjectsReturned:
            # error - no token (or more than one)
            return False

        if pilot:
            request.pilot = pilot

            # try to save user of the current job, when available
            # this allow the pilot to PATCH with the objs (m2m) info.
            job = pilot.get_current_job()
            if job:
                request.user = job.user

            return True

        return False # pragma: no cover
