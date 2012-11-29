from piston.handler import BaseHandler
from core.models import Application

class ApplicationHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Application

    def read(self, request, app_id=None):
        """
        Returns a single app if `app_id` is given,
        otherwise a subset.

        """
        base = Application.objects

        if app_id:
            return base.get(pk=app_id)
        else:
            return base.all() # Or base.filter(...)
