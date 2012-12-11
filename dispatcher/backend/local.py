# vim: tabstop=4 shiftwidth=4 softtabstop=4
import logging
logger = logging.getLogger(__name__)

from subprocess import Popen, PIPE
import os, signal
from urlparse import urlparse

from gooserver.settings import PROJECT_PATH

def submit(pilot):
    """
    submit a pilot job using local protocol
    """
    exec_path = os.path.join(PROJECT_PATH,'dispatcher/tools/goo-pilot.py')
    #TODO: FIX! (winckler)
    base_url = 'http://localhost:8000/api/v1/dispatcher/'
    print exec_path
    pid = Popen([exec_path, base_url, pilot.token], close_fds=True).pid
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
    pass
