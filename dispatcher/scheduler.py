# vim: tabstop=4 shiftwidth=4 softtabstop=4
from django.db.models import Q

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
        site.submit_pilot_based_on_job(job)

def match(pilot, time_left):
    """
    Select a job for a pilot
    - filter jobs to match requirements (status, hosts, cores)
    - evaluate users priority (and cache it)
    - select the highest priority job
    """
    # delay import to avoid ciclic reference
    from core.models import Job
    candidates = Job.objects.filter(Q(status = 'P'))

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
