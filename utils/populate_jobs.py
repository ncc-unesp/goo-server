#!/usr/bin/env python

from dateutil.relativedelta import relativedelta
from datetime import datetime
from gooserver import settings
from django.core.management  import setup_environ
from django.utils.timezone import utc
from time import timezone
import random
setup_environ(settings)

from core.models import Job

def get_month_range(date):
    year = date.year
    month = date.month
    first = datetime(year, month, 1)
    last = first + relativedelta(months = 1) - relativedelta(days=1)
    last = datetime(last.year, last.month, last.day, 23, 59, 59)
    return first, last

date = datetime(2011, 01, 01).replace(tzinfo=utc)
for i in range(0,20000):
    job = Job()
    job.name = 'foo'
    job.user_id = 1
    job.application_id = 1
    job.status = 'C'
    create = date + relativedelta(hours=random.uniform(0,17520)) # two years
    start = create + relativedelta(hours=random.uniform(0,6))
#    end = start + relativedelta(hours=random.gauss(12,8)) # 12 hours, 8 hours
    end = start + relativedelta(hours=random.gauss(360,240)) # 15 days, 10 days

    job.create_time = create
    job.start_time = start
    job.end_time = end
    job.save()
    print "done."
