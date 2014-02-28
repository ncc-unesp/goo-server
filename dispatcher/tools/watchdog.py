#!/usr/bin/env python
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


# Check to find dead jobs (started but doesn't have update in the
# last 2 hours)

from core.models import Job

from datetime import timedelta
from django.utils.timezone import now

limit = now() - timedelta(seconds=60*60*2) # 2 hours

for j in Job.objects.filter(status='R').filter(modification_time__lt=limit):
    # cancel pilot
    j.pilot = None

    # change state
    if j.restart:
        j.status = 'P'
    else:
        j.status = 'E'

    j.save()
