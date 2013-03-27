# vim: tabstop=4 shiftwidth=4 softtabstop=4

from tastypie.resources import ModelResource, Resource
from tastypie import fields
from django.db.models import Q
from core.models import *
from django.utils.timezone import utc

from tastypie.authorization import ReadOnlyAuthorization

from django.utils.timezone import now

from django.conf.urls import url
from tastypie.utils import trailing_slash

from dateutil.relativedelta import relativedelta
from datetime import datetime

class StatsJobs(object):
    def __init__(self, end, count):
        self.end = end
        self.count = count

class StatsJobsResource(Resource):
    """This resource handler stats requests.

    Allowed Methods:

        GET    /stats/jobs/          # Get stats about running jobs
    """

    end = fields.DateTimeField(attribute='end')
    count = fields.IntegerField(attribute='count')

    class Meta:
        resource_name = 'stats/jobs'
        #object_class = StatsJob
        #authentication = UserTokenAuthentication()
        authorization = ReadOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['']

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
