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
           (job.pph <= self.max_cores) and \
           (job.ttl <= self.max_time):
            return True
        else:
            return False

    def submit_pilot_based_on_job(self, job):
        if not self.is_job_acceptable(job):
            raise AttributeError

        p = Pilot()
        p.site = self
        p.cores = job.pph
        p.hosts = job.hosts
        p.memory = job.memory_requirement
        p.save()

        p.submit()

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
        job = scheduler.match(self, time_left)

        if not job:
            return None

        job.pilot = self
        job.status = 'R'
        job.save()

        return job

    def is_job_acceptable(self, job, time_left):
        if (job.hosts == self.hosts) and \
           (job.pph == self.cores) and \
           (job.ttl <= time_left):
            return True
        else:
            return False
