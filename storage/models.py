from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Object(models.Model):
    name = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=40, primary_key=True)
    size = models.PositiveIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    url = models.CharField(max_length=255)
    public = models.BooleanField(default=False)

    TYPE_CHOICES = (
        ('A', 'Application'),
        ('I', 'Input'),
        ('O', 'Output'),
        ('C', 'Checkpoint'),
        ('P', 'Progress'),
    )

    object_type = models.CharField(max_length=1,
                                   choices=TYPE_CHOICES,
                                   default='A')

    def __repr__ (self):
        return '<Object %s>' % self

    def __str__ (self):
        return self.name

class DataProxyServer(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)

    def __repr__ (self):
        return '<ObjectProxy %s>' % self

    def __str__ (self):
        return self.name
