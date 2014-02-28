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

from tastypie.resources import ModelResource, Resource
from tastypie import fields
from django.db.models import Q
from core.models import *
from django.utils.timezone import utc

from django.core.cache import cache

from tastypie.authorization import ReadOnlyAuthorization

from django.utils.timezone import now

from django.conf.urls import url
from tastypie.utils import trailing_slash

from dateutil.relativedelta import relativedelta
from datetime import datetime

import time

class StatsJobs(object):
    def __init__(self, date, value):
        self.date = date
        self.value = value

class AvgTimeJobs(object):
    def __init__(self, x, percent):
        self.x = x
        self.percent = percent

class StatsApps(object):
    def __init__(self, app, percent):
        self.app = app
        self.percent = percent

class Stats(object):
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

class GenericResource():
    def _get_month_range(self, date):
        """
        Return the first datetime in the given datetime month and the last
        datetime.
        """
        year = date.year
        month = date.month
        first = datetime(year, month, 1)
        last = first + relativedelta(months = 1) - relativedelta(days=1)
        last = datetime(last.year, last.month, last.day, 23, 59, 59)
        return first.replace(tzinfo=utc), last.replace(tzinfo=utc)

class StatsResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/general/      # Get general stats about the grid
    """

    name = fields.CharField(attribute='name')
    description = fields.CharField(attribute='description')
    value = fields.IntegerField(attribute='value')

    class Meta:
        resource_name = 'stats/general'
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['']

    def _get_queue_size(self):
        """
        Return the amount of jobs in queue, just now.
        """
        now = datetime.utcnow().replace(tzinfo=utc)
        cache_id = "jobs_queue"

        cached = cache.get(cache_id)
        if cached:
            count = cached
        else:
            jobs = Job.objects.filter(status='P') # Pending status
            count = jobs.count()
            cache.set(cache_id, count, 60*30) # 30 min cache

        return count

    def _get_quality(self):
        """
        Return the quality of service in the current month.
        """
        now = datetime.utcnow().replace(tzinfo=utc)
        begin, end = self._get_month_range(now)
        cache_id = "quality"

        cached = cache.get(cache_id)
        if cached:
            quality = cached
        else:
            jobs = Job.objects.filter(create_time__gte=begin)
            jobs = jobs.filter(create_time__lte=end).filter(status='C')

            quality = 0
            for job in jobs:
                diff1 = job.end_time - job.start_time
                diff2 = job.end_time - job.create_time
                quality += diff1.total_seconds() / diff2.total_seconds()

            count = jobs.count()
            if count is not 0:
                quality = quality / jobs.count()

            cache.set(cache_id, quality, 60*30) # 30 min cache

        return quality


    def _get_running_jobs(self):
        """
        Return the amount of jobs runing, just now.
        """
        now = datetime.utcnow().replace(tzinfo=utc)
        cache_id = "jobs_running"

        cached = cache.get(cache_id)
        if cached:
            count = cached
        else:
            jobs = Job.objects.filter(status='R') # Running status
            count = jobs.count()
            cache.set(cache_id, count, 60*30) # 30 min cache

        return count

    def _get_avg_time(self):
        """
        Return the average of running time of completed jobs in the current
        mounth.
        """
        now = datetime.utcnow().replace(tzinfo=utc)
        begin, end = self._get_month_range(now)
        cache_id = "avg_time"

        cached = cache.get(cache_id)
        if cached:
            avg_time = cached
        else:
            jobs = Job.objects.filter(create_time__gte=begin)
            jobs = jobs.filter(create_time__lte=end).filter(status='C')

            avg_time = 0
            for job in jobs:
                diff = job.end_time - job.start_time
                avg_time += diff.total_seconds()

            count = jobs.count()
            if count is not 0:
                avg_time = avg_time / obs.count()

            cache.set(cache_id, avg_time, 60*30) # 30 min cache

        return avg_time


    def _get_processed_hours(self, request=None, **kwargs):
        """
        Return the amount of hours that our cluster processed in current month.
        """
        now = datetime.utcnow().replace(tzinfo=utc)
        begin, end = self._get_month_range(now)
        cache_id = "processed_hours"

        cached = cache.get(cache_id)
        if cached:
            processed_hours = cached
        else:
            jobs = Job.objects.filter(Q(end_time__range=[begin, end]) | \
                                      Q(start_time__range=[begin, end]) | \
                                      Q(start_time__lte=begin) & \
                                      Q(end_time__gte=end))

            processed_hours = 0
            for job in jobs:
                if job.end_time is None:
                    end_time = end
                else:
                    end_time = min(end, job.end_time)

                if job.start_time is None:
                    start_time = begin
                else:
                    start_time = max(begin, job.start_time)

                d = end_time - start_time
                processed_hours += (d.seconds*job.hosts*job.cores_per_host)/60**2

            cache.set(cache_id, processed_hours, 60*30) # 30 min cache

        return processed_hours


    def obj_get_list(self, request=None, **kwargs):

        values = {'queue': ['Jobs in queue', self._get_queue_size()],
                  'running': ['Running jobs', self._get_running_jobs()],
                  'quality': ['Quality of service', self._get_quality()],
                  'avg_time': ['Quality of service', self._get_quality()],
                  'hours': ['Processed Hours', self._get_processed_hours()]}

        results = []
        for v in values.items():
            results.append(Stats(v[0], v[1][0], v[1][1]))

        return results


    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle



class StatsJobsResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/jobs/          # Get stats about running jobs
    """

    date = fields.DateTimeField(attribute='date')
    value = fields.IntegerField(attribute='value')

    class Meta:
        resource_name = 'stats/jobs'
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['']


    def obj_get_list(self, request=None, **kwargs):
        """
        Return a list of all jobs that:
            end_time is in range OR
            begin_time is in range OR
            (begin_time <= begin AND
             end_time >= end)
        """
        now = datetime.utcnow().replace(tzinfo=utc)
        results = []

        for i in range(0,12):
            begin, end = self._get_month_range(now - relativedelta(months = i))
            jobs = Job.objects.filter(Q(end_time__range=[begin, end]) | \
                                      Q(start_time__range=[begin, end]) | \
                                      Q(start_time__lte=begin) & \
                                      Q(end_time__gte=end))


            stat = StatsJobs(end, jobs.count())
            results.append(stat)

        return results

    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle

class StatsHoursResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/hours/          # Get stats about running jobs in
                                        processed hours
    """

    date = fields.DateTimeField(attribute='date')
    value = fields.IntegerField(attribute='value')

    class Meta:
        resource_name = 'stats/hours'
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['']

    def obj_get_list(self, request=None, **kwargs):
        """
        Return a list of all jobs that:
            end_time is in range OR
            begin_time is in range OR
            (begin_time <= begin AND
             end_time >= end)
        """
        now = datetime.utcnow().replace(tzinfo=utc)

        results = []
        for i in range(0,12):
            begin, end = self._get_month_range(now - relativedelta(months = i))

            cache_id = "%d_%s_%s" % (i, time.mktime(begin.timetuple()),
                                                    time.mktime(end.timetuple()))

            cached = cache.get(cache_id)
            if cached:
                results.append(cached)
            else:
                jobs = Job.objects.filter(Q(end_time__range=[begin, end]) | \
                                          Q(start_time__range=[begin, end]) | \
                                          Q(start_time__lte=begin) & \
                                          Q(end_time__gte=end))

                count = 0
                for job in jobs:
                    if job.end_time is None:
                        end_time = end
                    else:
                        end_time = min(end, job.end_time)

                    if job.start_time is None:
                        start_time = begin
                    else:
                        start_time = max(begin, job.start_time)

                    delta = end_time - start_time
                    count += (delta.seconds*job.hosts*job.cores_per_host)/60**2

                stat = StatsJobs(end, count)
                results.append(stat)

                cache.set(cache_id, stat, 60*30) # 30 min cache

        return results

    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle

class StatsAvgTimeResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/avgtime/       # Get stats about avg running time
    """

    x = fields.CharField(attribute='x')
    percent = fields.FloatField(attribute='percent')

    class Meta:
        resource_name = 'stats/avgtime'
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['']

    def obj_get_list(self, request=None, **kwargs):
        #now = datetime.utcnow().replace(tzinfo=utc)
        now = datetime(2011,1,1).replace(tzinfo=utc)
        begin, end = self._get_month_range(now)

        cache_id = "avgtime"

        cached = cache.get(cache_id)
        if cached:
            jobs = cached
        else:
            jobs = Job.objects.filter(create_time__gte=begin)
            jobs = jobs.filter(create_time__lte=end).filter(status='C')
            cache.set(cache_id, jobs, 60*30) # 30 min cache

        ranges = [['<6hours',  0],
                  ['<24hours', 0],
                  ['<72hours', 0],
                  ['>72hours', 0]]

        for job in jobs:
            diff = job.end_time - job.start_time
            diff = diff.total_seconds()
            if diff <= 21600:
                ranges[0][1] += 1
            elif diff <= 86400:
                ranges[1][1] += 1
            elif diff <= 259200:
                ranges[2][1] += 1
            else:
                ranges[3][1] += 1

        count = jobs.count()
        results = []
        for r in ranges:
            try:
                percent = r[1] / float(count)
            except ZeroDivisionError:
                percent = 0
            stat = AvgTimeJobs(r[0], percent)
            results.append(stat)
        return results

    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle

class StatsAppsResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/apps/       # Get stats about applications
    """

    app = fields.CharField(attribute='app')
    percent = fields.FloatField(attribute='percent')

    class Meta:
        resource_name = 'stats/apps'
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['']

    def obj_get_list(self, request=None, **kwargs):
        #now = datetime.utcnow().replace(tzinfo=utc)
        now = datetime(2011,1,1).replace(tzinfo=utc)
        begin, end = self._get_month_range(now)

        cache_id = "statsapp"

        cached = cache.get(cache_id)
        if cached:
            results = cached
        else:
            jobs = Job.objects.filter(create_time__gte=begin)
            jobs = jobs.filter(create_time__lte=end).filter(status='C')

            apps = {}
            results = []
            count = jobs.count()

            for job in jobs:
                app = job.application._name
                apps[app] = 1 if not apps.has_key(app) else apps[app] + 1

            for app in apps:
                percent = (apps[app] * 100) / float(count)
                stat = StatsApps(app, percent)
                results.append(stat)

            cache.set(cache_id, results, 60*30) # 30 min cache

        return results

    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle
