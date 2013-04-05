# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import utc
from datetime import timedelta, datetime
from django.utils.timezone import now

import uuid
from dispatcher.models import Pilot
from storage.models import Object

from dispatcher import scheduler

import logging
logger = logging.getLogger(__name__)

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
    _name = models.CharField(max_length=255)
    _version = models.CharField(max_length=63)

    # description about the application
    _description = models.TextField(default='')
    # help text about the usage of this version
    _usage = models.TextField(default='')

    # if is public
    _public = models.BooleanField(default=True)

    executable = models.CharField(max_length=512) # if custom
    _app_obj = models.ForeignKey(Object, null=True, related_name='application_set')
    args = models.CharField(max_length=512)

    # Files
    inputs = models.CharField(max_length=512) # gerar o input_obj_id
    outputs = models.CharField(max_length=512)
    checkpoints = models.CharField(max_length=512)

    # Capabilities
    _multi_hosts = models.BooleanField(default='False') # MPI
    _multi_thread = models.BooleanField(default='False') # SMP
    _shared_fs = models.BooleanField(default='False')

    # Hints for template creation
    _constant_fields = models.CharField(max_length=1024, default='')
    _required_fields = models.CharField(max_length=1024, default='')

    # Default values
    hosts = models.PositiveIntegerField(default=1)
    cores_per_host = models.PositiveIntegerField(default=1)
    maxtime = models.PositiveIntegerField(default=43200) # 12 hours
    diskspace = models.PositiveIntegerField(default=2048) # 2GB
    memory = models.PositiveIntegerField(default=2048) # 2GB

    def __repr__ (self): # pragma: no cover
        return '<Application %s>' % self

    def __str__ (self):
        return '%s %s' % (self._name, self._version)

    def get_constant_fields(self):
        """
        Return a list of field that values are enforced by application.
        """
        if self._constant_fields:
            return map(unicode.strip, self._constant_fields.split(','))
        else:
            return []

    def get_required_fields(self):
        """
        Return a list of fields required for filled by user.
        Some fields, are required but not return in this method, because
        are overwrite by default values.
        """
        if self._required_fields:
            return map(unicode.strip, self._required_fields.split(','))
        else:
            return []

class Job(models.Model):
    name = models.CharField(max_length=20, blank=False)
    application = models.ForeignKey(Application)
    # 0-100 (%) value or -1 when not available
    progress = models.PositiveIntegerField(default='', null=True, blank=True)
    hosts = models.PositiveIntegerField(default=1)
    cores_per_host = models.PositiveIntegerField(default=1)
    priority = models.PositiveIntegerField(default=0)
    restart = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    # values for execution that could be customized
    executable = models.CharField(max_length=512)
    args = models.CharField(max_length=512)
    inputs = models.CharField(max_length=512)
    outputs = models.CharField(max_length=512)
    checkpoints = models.CharField(max_length=512)

    # objects id
    input_objs = models.ManyToManyField(Object, null=True, related_name='input_for')
    output_objs = models.ManyToManyField(Object, null=True, related_name='output_for')
    checkpoint_objs = models.ManyToManyField(Object, null=True, related_name='checkpoint_for')

    # max seconds to run
    maxtime = models.PositiveIntegerField(default=43200) # 12 hours

    # MegaBytes
    diskspace = models.PositiveIntegerField(default=2048) # 2GB
    memory = models.PositiveIntegerField(default=2048) # 2GB

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
    diskspace_in_use = models.PositiveIntegerField(default=0)
    memory_in_use = models.PositiveIntegerField(default=0)

    # aka tail -f
    progress_string = models.TextField(default='')

    eta = models.PositiveIntegerField(null=True, default=None)
    return_code = models.IntegerField(null=True, default=None)
    #create_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
    modification_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)

    pilot = models.ForeignKey(Pilot, default=None, null=True)

    def save(self, *args, **kwargs):
        # enforce application constants
        if self.application:
            for attr in self.application.get_constant_fields():
                value = getattr(self.application, attr)
                setattr(self, attr, value)

        # get the last state to get some action
        if not self.id:
            # new object
            last_status = None
        else:
            old_self = Job.objects.get(pk=self.id)
            last_status = old_self.status

        super(Job, self).save(*args, **kwargs)
        new_self = Job.objects.get(pk=self.id)

        if (self.status == 'P') and (last_status != 'P'):
            # welcome! let find a nice place for you
            try:
                scheduler.allocate(new_self)
            except scheduler.NoMatchError:
                # no sites match job requirement
                self.status = 'E'
                self.save()
                return


        if (self.status == 'D') and (last_status == 'R'):
            # before delete, cancel
            self.pilot.cancel()

        # TODO: notify user, if requested
        # and log
        if (self.status != last_status):
            logger.info('Job %d changed status from %s to %s'
                             % (self.id, last_status, self.status))

    def delete(self, *args, **kwargs):
        self.status = 'D'
        self.save()
