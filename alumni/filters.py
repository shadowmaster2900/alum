from django.contrib.admin import SimpleListFilter
from .models import Alumni

class MajorFilter(SimpleListFilter):
    title = 'major'
    parameter_name = 'major'

    def lookups(self, request, model_admin):
        majors = set([alumni.major for alumni in Alumni.objects.all()])
        return [(major, major) for major in majors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(major=self.value())
        return queryset

class LocationFilter(SimpleListFilter):
    title = 'location'
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        locations = set([alumni.location for alumni in Alumni.objects.all()])
        return [(location, location) for location in locations]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(location=self.value())
        return queryset

class MaritalStatusFilter(SimpleListFilter):
    title = 'marital status'
    parameter_name = 'marital_status'

    def lookups(self, request, model_admin):
        statuses = set([alumni.marital_status for alumni in Alumni.objects.all()])
        return [(status, status) for status in statuses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(marital_status=self.value())
        return queryset
