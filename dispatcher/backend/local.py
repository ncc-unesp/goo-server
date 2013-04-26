# vim: tabstop=4 shiftwidth=4 softtabstop=4
import logging
logger = logging.getLogger(__name__)

from subprocess import Popen, PIPE
import os, signal
from urlparse import urlparse

from django.conf import settings

def submit(pilot):
    """
    submit a pilot job using local protocol
    """
    exec_path = os.path.join(settings.PROJECT_PATH,'dispatcher/tools/goo-pilot.py')
    url = settings.BASE_URL
    pid = Popen([exec_path, url, pilot.token],
                close_fds=True, stdout=PIPE, stderr=PIPE).pid
    pilot.url = 'local://%d' % pid
    pilot.save()

    logger.info('Sending job')

def cancel(pilot):
    """
    cancel a pilot job using local protocol
    """
    url = urlparse(pilot.url)
    os.kill(int(url.netloc), signal.SIGTERM)
    logger.info('Cancel job')
