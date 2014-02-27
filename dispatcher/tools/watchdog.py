#!/usr/bin/env python
# check to find dead jobs (started but doesn't have update in the last 2 hours)

from core.models import Job

from datetime import timedelta
from django.utils.timezone import now

limit = now() - timedelta(seconds=60*60*2) # 2 hours

for j in Job.objects.filter(status='R').filter(modification_time__lt=limit):
    # cancel pilot
    j.pilot = None

    # change state
    if j.restart:
        j.status = 'P'
    else:
        j.status = 'E'

    j.save()
