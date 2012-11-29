from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    priority = models.PositiveIntegerField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Application(models.Model):
    """Bla bla bla."""

    name = models.CharField(max_length=255)

class Version(models.Model):
    version = models.CharField(max_length=20)
    application = models.ForeignKey(Application)

class Type(models.Model):
    name = models.CharField(max_length=20)
    version = models.ForeignKey(Version)
    executable = models.CharField(max_length=512)
    obj_app_id = models.CharField(max_length=512)
    args = models.CharField(max_length=512)

    # Files
    inputs = models.CharField(max_length=512)
    outputs = models.CharField(max_length=512)
    checkpoints = models.CharField(max_length=512)

    # Capabilities
    multi_hosts = models.BooleanField(default='False')
    multi_thread = models.BooleanField(default='False')
    shared_fs = models.BooleanField(default='False')

class Job(models.Model):
    name = models.CharField(max_length=20)
    type = models.ForeignKey(Version)
    progress = models.PositiveIntegerField()
    hosts = models.PositiveIntegerField()
    pph = models.PositiveIntegerField()
    priority = models.PositiveIntegerField()
    restart = models.BooleanField(default='False')
    notify = models.BooleanField(default='False')
    user = models.ForeignKey(User)

    # objects id
    input_obj_id = models.CharField(max_length=512)
    output_obj_id = models.CharField(max_length=512)
    checkpoing_obj_id = models.CharField(max_length=512)

    # max seconds to run
    ttl = models.PositiveIntegerField()

    # MegaBytes
    disk_requirement = models.PositiveIntegerField()
    memory_requirement = models.PositiveIntegerField()

    # Status info
    STATUS_CHOICES = (
        ('P', 'Pendding'),
        ('R', 'Running'),
        ('C', 'Completed'),
        ('D', 'Deleted'),
        ('E', 'Error'),
    )

    status = models.CharField(max_length=1,
                             choices=STATUS_CHOICES,
                             default='P')
    # MegaBytes
    disk_in_use = models.PositiveIntegerField()
    memory_in_use = models.PositiveIntegerField()

    eta = models.PositiveIntegerField()
    return_code = models.IntegerField()
    create_time = models.DateTimeField(auto_now=True)
    modification_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
