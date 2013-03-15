# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.db import models
import uuid
from urlparse import urlparse

class Site(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=512)

    max_cores = models.PositiveIntegerField()
    max_hosts = models.PositiveIntegerField()
    max_time = models.PositiveIntegerField()

    def is_job_acceptable(self, job):
        if (job.hosts <= self.max_hosts) and \
           (job.cores_per_host <= self.max_cores) and \
           (job.maxtime <= self.max_time):
            return True
        else:
            return False

    def submit_pilot_based_on_job(self, job):
        if not self.is_job_acceptable(job):
            raise AttributeError

        p = Pilot()
        p.site = self
        p.cores = job.cores_per_host
        p.hosts = job.hosts
        p.memory = job.memory
        p.save()

        p.submit()

        return p

import backend
import scheduler
class Pilot(models.Model):
    site = models.ForeignKey(Site)
    url = models.CharField(max_length=512)
    token = models.CharField(max_length=512)

    cores = models.PositiveIntegerField()
    hosts = models.PositiveIntegerField()

    # MegaBytes
    memory = models.PositiveIntegerField()

    def save(self, *args, **kvargs):
        if not self.token:
            self.token = unicode(uuid.uuid4())

        super(Pilot, self).save(*args, **kvargs)

    def submit(self):
        return self._get_backend_method('submit')(self)

    def cancel(self):
        return self._get_backend_method('cancel')(self)

    def _get_backend_method(self, method):
        scheme = urlparse(self.site.url).scheme
        try:
            module = getattr(backend, scheme)
            return getattr(module, method)
        except AttributeError:
            raise NotImplementedError

    def get_new_job(self, time_left):
        # check if is already executing a job
        if self.get_current_job():
            raise StopIteration

        job = scheduler.match(self, time_left)

        if not job:
            raise StopIteration

        job.pilot = self
        job.status = 'R'
        job.save()

        return job

    def is_job_acceptable(self, job, time_left):
        if (job.hosts == self.hosts) and \
           (job.cores_per_host == self.cores) and \
           (job.maxtime <= time_left):
            return True
        else:
            return False

    def get_current_job(self):
        # can raise self.MultipleObjectsReturned
        # this means DB inconsistency

        try:
            return self.job_set.filter(status='R').get()
        except self.job_set.model.DoesNotExist:
            return None
