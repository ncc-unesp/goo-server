# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.db import models
from django.contrib.auth.models import User

from datetime import timedelta
from django.utils.timezone import now

import uuid
from dispatcher.models import Pilot
from storage.models import Object

class UserFunctions:
    def get_jobs(self):
        return Job.objects.filter(user=self)

User.__bases__ += (UserFunctions,)

class UserToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=512)
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField()

    def save(self, *args, **kvargs):
        if not self.token:
            self.token = uuid.uuid4()

        if not self.expire_time:
            self.expire_time = now() + timedelta(days=30)

        super(UserToken, self).save(*args, **kvargs)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    priority = models.PositiveIntegerField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Application(models.Model):
    """Bla bla bla."""

    name = models.CharField(max_length=255)

    def __repr__ (self): # pragma: no cover
        return '<Application %s>' % self

    def __str__ (self):
        return self.name

class Version(models.Model):
    version = models.CharField(max_length=20)
    application = models.ForeignKey(Application)

    def __repr__ (self): # pragma: no cover
        return '<Version %s>' % self

    def __str__ (self):
        return '%s %s' % (self.application, self.version)

class Type(models.Model):
    name = models.CharField(max_length=20)
    version = models.ForeignKey(Version)
    executable = models.CharField(max_length=512) # if custom
    app_obj = models.ForeignKey(Object, null=True, related_name='application_set')
    args = models.CharField(max_length=512)

    # Files
    inputs = models.CharField(max_length=512) # gerar o input_obj_id
    outputs = models.CharField(max_length=512)
    checkpoints = models.CharField(max_length=512)

    # Capabilities
    multi_hosts = models.BooleanField(default='False') # MPI
    multi_thread = models.BooleanField(default='False') # SMP
    shared_fs = models.BooleanField(default='False')


    def __repr__ (self): # pragma: no cover
        return '<Type %s>' % self

    def __str__ (self):
        return '%s %s' % (self.version, self.name)

class Job(models.Model):
    name = models.CharField(max_length=20, blank=False)
    type = models.ForeignKey(Type)
    progress = models.PositiveIntegerField(default=0)
    hosts = models.PositiveIntegerField(default=1)
    pph = models.PositiveIntegerField(default=1)
    priority = models.PositiveIntegerField(default=0)
    restart = models.BooleanField(default='False')
    user = models.ForeignKey(User)

    # values for execution that could be customized
    executable = models.CharField(max_length=512)
    args = models.CharField(max_length=512)
    inputs = models.CharField(max_length=512)
    outputs = models.CharField(max_length=512)
    checkpoints = models.CharField(max_length=512)
    app_objs = models.ForeignKey(Object, null=True, related_name='app_for')

    # objects id
    input_objs = models.ManyToManyField(Object, null=True, related_name='input_for')
    output_objs = models.ManyToManyField(Object, null=True, related_name='output_for')
    checkpoint_objs = models.ManyToManyField(Object, null=True, related_name='checkpoint_for')

    # max seconds to run
    ttl = models.PositiveIntegerField(default=43200) # 12 hours

    # MegaBytes
    disk_requirement = models.PositiveIntegerField(default=2048) # 2GB
    memory_requirement = models.PositiveIntegerField(default=2048) # 2GB

    # Status info
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('R', 'Running'),
        ('C', 'Completed'),
        ('D', 'Deleted'),
        ('E', 'Error'),
        ('B', 'Blocked'),
    )

    status = models.CharField(max_length=1,
                             choices=STATUS_CHOICES,
                             default='P')
    # for future use on DAG workflow
    parent = models.ManyToManyField('self', symmetrical=False)

    # MegaBytes
    disk_in_use = models.PositiveIntegerField(default=0)
    memory_in_use = models.PositiveIntegerField(default=0)

    # aka tail -f
    progress_string = models.TextField(default='')

    eta = models.PositiveIntegerField(null=True, default=None)
    return_code = models.IntegerField(null=True, default=None)
    create_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)

    pilot = models.ForeignKey(Pilot, default=None, null=True)
