from django.http import HttpResponseForbidden
from piston.utils import rc

#TODO: Check if token is valid
def check_token(function):
    """
    Make another a function more beautiful.
    """
    def _decorated(*args, **kwargs):
        request = args[1]
        token = request.REQUEST.get('token', None)

        if token is None:
            #resp = rc.BAD_REQUEST
            #resp.write("Please, provide a token.")
            data = { "return": 401 }
            response = HttpResponse(data)
            return response
            #return resp
            #return HttpResponseForbidden('Please provide a token.')
        return function(*args, **kwargs)
    return _decorated
