from django.conf import settings
from django.contrib.auth.models import User, check_password
from core.models import UserToken
from datetime import datetime
from django.utils.timezone import utc

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

#class UserTokenBackend(object):
#    """
#    Authenticate user with a token.
#    """

#    def authenticate(self, token=None):
#        # check if token exists inside the request
#        if token is None:
#            return None

#        try:
#            # query DB for token and return user
#            tokens = UserToken.objects.filter(expire_time__gt=datetime.now().replace(tzinfo=utc))
#            return tokens.get(token=token).user

#        except UserToken.DoesNotExist, UserToken.MultipleObjectsReturned:
#            # error - no token (or more than one)
#            return None

#    def get_user(self, user_id):
#        try:
#            return User.objects.get(pk=user_id)
#        except User.DoesNotExist:
#            return None


class UserTokenAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # check if token exists inside the request
        if not request.REQUEST['token']:
            return False
        token = request.REQUEST['token']

        try:
            # query DB for token and return user
            t = UserToken.objects.filter(expire_time__gt=datetime.now())
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

#class UserTokenAuthorization(Authorization):
#    def is_authorized(self, request, object=None):
#        if request.user.date_joined.year == 2010:
#            return True
#        else:
#            return False

#    # Optional but useful for advanced limiting, such as per user.
#    def apply_limits(self, request, object_list):
#        if request and hasattr(request, 'user'):
#            return object_list.filter(author__username=request.user.username)

#        return object_list.none()
