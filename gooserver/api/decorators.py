from piston.utils import rc
from django.contrib.auth import authenticate, login

def check_token(function):
    """
    Make another a function more beautiful.
    """
    def _decorated(*args, **kwargs):
        request = args[1]
        token = request.REQUEST.get('token', None)
        user = authenticate(token=token)
        if user is not None:
            login(request, user)
            return function(*args, **kwargs)
        else:
            return rc.FORBIDDEN

    return _decorated
