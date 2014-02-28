# This file is part of goo-server.
#
# Copyright (c) 2103-2014 by Núcleo de Computação Científica, UNESP
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
from django.db import models
from django.contrib.auth.models import User

class DataProxyServer(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=512)

    def __repr__ (self):
        return '<DataObjectProxy %s>' % self

    def __str__ (self):
        return self.name

class DataObject(models.Model):
    name = models.CharField(max_length=255)
    sha1 = models.CharField(max_length=40)
    size = models.PositiveIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    data_proxy_servers = models.ManyToManyField(DataProxyServer, blank=True)
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
        return '<DataObject %s>' % self

    def __str__ (self):
        return self.name
