# vim: tabstop=4 shiftwidth=4 softtabstop=4
from subprocess import Popen, PIPE, call, check_output
import os

from gooserver.settings import PROJECT_PATH, BASE_URL

import logging
logger = logging.getLogger(__name__)

# fix python undefined behavior
# http://bugs.python.org/issue9374
import urlparse

def register_scheme(scheme):
    for method in filter(lambda s: s.startswith('uses_'), dir(urlparse)):
        getattr(urlparse, method).append(scheme)

register_scheme('globus')


class GridProxyError(Exception):
    pass

def check_proxy(fn):
    def _f(*args, **kwargs):
        devnull = open(os.devnull, 'w')
        ret_code = call(["/usr/bin/grid-proxy-info"],
                        close_fds=True, stdout=devnull, stderr=devnull)
        if (ret_code != 0):
            raise GridProxyError

        return fn(*args, **kwargs)
    return _f

@check_proxy
def submit(pilot):
    """
    submit a pilot job using GRAM protocol
    """
    
    site_addr = urlparse.urlparse(pilot.site.url)

    exec_path = os.path.join(PROJECT_PATH,'dispatcher/tools/goo-pilot.py')
    url = BASE_URL + '/api/v1/'

    # globus-job-submit ce.grid.unesp.br/jobmanager-pbs -x (queue=long) -s /usr/bin/id args
    cmd = ['/usr/bin/globus-job-submit',
           '%s%s' % (site_addr.hostname, site_addr.path), 
           '-x', '(%s)' % site_addr.query, 
           '-s', exec_path, url, pilot.token]

    devnull = open(os.devnull, 'w')
    # can raise CalledProcessError
    job_url = check_output(cmd, close_fds=True, stderr=devnull).strip()
    
    pilot.url = job_url
    pilot.save()

    logger.info('Sending job')

@check_proxy
def cancel(pilot):
    """
    cancel a pilot job using GRAM protocol
    """

    devnull = open(os.devnull, 'w')

    call(['/usr/bin/globus-job-cancel', '-f', pilot.url],
         close_fds=True, stdout=devnull, stderr=devnull)

    call(['/usr/bin/globus-job-clean', '-f', pilot.url],
         close_fds=True, stdout=devnull, stderr=devnull)
    
    logger.info('Cancel job')
