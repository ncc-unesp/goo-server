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
                                      Q(start_time__lte=begin) & Q(end_time__gte=end))


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

            cache_id = "%d_%s_%s" % (i, time.mktime(begin.timetuple()), time.mktime(end.timetuple()))

            cached = cache.get(cache_id)
            if cached:
                results.append(cached)
            else:
                jobs = Job.objects.filter(Q(end_time__range=[begin, end]) | \
                                          Q(start_time__range=[begin, end]) | \
                                          Q(start_time__lte=begin) & Q(end_time__gte=end))

                count = 0
                for job in jobs:
                    end_time = end if job.end_time is None else min(end, job.end_time)
                    start_time = begin if job.start_time is None else max(begin, job.start_time)
                    delta = end_time - start_time
                    count += (delta.seconds * job.hosts * job.cores_per_host) / 60 ** 2

                stat = StatsJobs(end, count)
                results.append(stat)

                cache.set(cache_id, stat, 60*30) # 30 min cache

        return results

    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle

class StatsQualityResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/quality/          # Get stats about quality of service
    """

    date = fields.DateTimeField(attribute='date')
    value = fields.FloatField(attribute='value')

    class Meta:
        resource_name = 'stats/quality'
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
        #now = datetime(2011,1,1).replace(tzinfo=utc)
        begin, end = self._get_month_range(now)

        cache_id = "quality_%s_%s" % (time.mktime(begin.timetuple()), time.mktime(end.timetuple()))

        cached = cache.get(cache_id)
        if cached:
            jobs = cached
        else:
            jobs = Job.objects.filter(create_time__gte=begin).filter(create_time__lte=end).filter(status='C')
            cache.set(cache_id, jobs, 60*30) # 30 min cache

        quality = 0
        for job in jobs:
            diff1 = job.end_time - job.start_time
            diff2 = job.end_time - job.create_time
            quality += diff1.total_seconds() / diff2.total_seconds()

        count = jobs.count()
        if count is not 0:
            quality = quality / jobs.count()

        results = []
        stat = StatsJobs(end, quality)
        results.append(stat)

        return results

    def dehydrate(self, bundle):
        del bundle.data['resource_uri']
        return bundle

class StatsQueueResource(Resource, GenericResource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/queue/       # Get stats about jobs in queue
    """

    date = fields.DateTimeField(attribute='date')
    value = fields.IntegerField(attribute='value')

    class Meta:
        resource_name = 'stats/queue'
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
        #now = datetime(2011,1,1).replace(tzinfo=utc)
        #begin, end = self._get_month_range(now)

        cache_id = "queue_%s" % time.mktime(now.timetuple())

        cached = cache.get(cache_id)
        if cached:
            jobs = cached
        else:
            jobs = Job.objects.filter(status='P') # Pending
            cache.set(cache_id, jobs, 60*30) # 30 min cache

        count = jobs.count()
        results = []
        stat = StatsJobs(now, count)
        results.append(stat)

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
            jobs = Job.objects.filter(create_time__gte=begin).filter(create_time__lte=end).filter(status='C')
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
            percent = r[1] / float(count)
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
            jobs = Job.objects.filter(create_time__gte=begin).filter(create_time__lte=end).filter(status='C')

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
