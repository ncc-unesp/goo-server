# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.db import models
import uuid

class Site(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=512)

    max_cores = models.PositiveIntegerField()
    max_hosts = models.PositiveIntegerField()
    max_time = models.PositiveIntegerField()

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
            self.token = uuid.uuid4()

        super(Pilot, self).save(*args, **kvargs)
