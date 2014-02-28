# This file is part of goo-server.
#
# Copyright (c) 2103-2014 by Núcleo de Computação Científica, UNESP
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
