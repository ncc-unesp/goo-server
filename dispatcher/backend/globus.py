# This file is part of goo-server.
#
# Copyright (c) 2103-2014 by Nucleo de Computacao Cientifica, UNESP
#
# Authors:
#    Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#    Gabriel von. Winckler <winckler AT ncc DOT unesp DOT br>
#
# goo-server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# goo-server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
from subprocess import Popen, PIPE, call, check_output
import os

from django.conf import settings

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
    args_globus_cmd = ['/usr/bin/globus-job-submit']

    site_addr = urlparse.urlparse(pilot.site.url)
    args_site = ['%s%s' % (site_addr.hostname, site_addr.path)]

    job_rsl = '(jobType=single)(host_xcount=%d)(xcount=%d)' % (pilot.hosts, pilot.cores)
    args_rsl = [ '-x', '%s(%s)' % (job_rsl, site_addr.query) ]

    args_lease_time = ['-env', 'GOO_LEASE_TIME=%d' % pilot.site.max_time]

    # shared filesystem quickfix (gridunesp specific)
    args_tmp_dir = []
    if pilot.hosts > 1:
        args_tmp_dir = ['-env', 'GOO_TMPDIR=/store']

    exec_path = os.path.join(settings.PROJECT_PATH,'dispatcher/tools/goo-pilot.py')
    url = settings.BASE_URL
    args_exec = ['-s', exec_path, url, pilot.token]

    # globus-job-submit ce.grid.unesp.br/jobmanager-pbs -x (queue=long) -s /usr/bin/id args
    cmd = args_globus_cmd + args_site + args_rsl \
          + args_lease_time + args_tmp_dir + args_exec

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
