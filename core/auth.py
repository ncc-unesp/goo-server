# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf import settings
from django.contrib.auth.models import User, check_password
from core.models import UserToken

from django.utils.timezone import now

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

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
