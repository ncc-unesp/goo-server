# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf import settings
from django.contrib.auth.models import User, check_password
from core.models import UserToken

from django.utils.timezone import now

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

class DebugBackend(object):
    """
    Fake authentication enabled only on debug mode.
    user: 'root'
    passwd: *
    """

    def authenticate(self, username=None, password=None):
        if settings.DEBUG and username == 'root':
            try:
                user = User.objects.get(username='root')
            except User.DoesNotExist:
                # Create a new user.
                user = User(username='root', password='why?')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        if not settings.DEBUG:
            return None
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

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

        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username
