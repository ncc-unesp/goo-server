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
import threading

class NoMatchError(Exception):
    pass

def allocate(job):
    """
    Generate pilots
    - Select candidate sites based on job requirements
    - Create and send pilots to one or more sites
    """
    # delay import to avoid ciclic reference
    from dispatcher.models import Site
    candidates = filter(lambda s: s.is_job_acceptable(job), Site.objects.all())

    #TODO: select just the better sites
    #for now, selecting all

    if not candidates:
        raise NoMatchError

    for site in candidates:
        threading.Thread(target=Site.submit_pilot_based_on_job,
                                               args=(site, job)).start()
        #site.submit_pilot_based_on_job(job)

def match(pilot, time_left):
    """
    Select a job for a pilot
    - filter jobs to match requirements (status, hosts, cores)
    - evaluate users priority (and cache it)
    - select the highest priority job
    """
    # delay import to avoid ciclic reference
    from core.models import Job
    candidates = Job.objects.filter(status = 'P')

    _f = lambda job: pilot.is_job_acceptable(job, time_left)
    candidates = filter(_f, candidates)

    if not candidates:
        # no jobs found
        raise StopIteration

    return max(candidates, key=job_priority)

def job_priority(job):
    #TODO: select based on user priority
    # fifo for now
    return -int(job.create_time.strftime('%s'))
