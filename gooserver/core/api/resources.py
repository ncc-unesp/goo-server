from tastypie.resources import ModelResource
from tastypie import fields
from django.db.models import Q
from core.models import *

class TypeResource(ModelResource):
    class Meta:
        queryset = Type.objects.all()
        resource_name = 'type'

class ApplicationResource(ModelResource):
    class Meta:
        queryset = Type.objects.all()
        resource_name = 'apps'
        fields = ['id', 'name', 'multi_hosts', 'multi_thread',]
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]

    def dehydrate_name(self, bundle):
        return bundle.obj

#    def dehydrate(self, bundle):
#        bundle.data['custom_field'] = "Whatever you want"
#        return bundle

class JobResource(ModelResource):
    class Meta:
        # Remove from query deleted jobs
        queryset = Job.objects.filter(~Q(status = 'D'))
        resource_name = 'jobs'
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['get',]
        list_exclude = ['return_code', 'hosts', 'eta', 'input_obj_id',
                        'output_obj_id', 'memory_in_use', 'memory_requirement',
                        'start_time', 'restart', 'ttl', 'pph',
                        'checkpoing_obj_id', 'disk_requirement', 'disk_in_use',
                        'create_time', 'end_time', 'modification_time', ]

    def dehydrate(self, bundle):
        if self.get_resource_uri(bundle) != bundle.request.path:
            list_exclude = self._meta.list_exclude
            for item in list_exclude:
                del bundle.data[item]
        return bundle
