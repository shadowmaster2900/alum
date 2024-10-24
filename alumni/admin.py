from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import School, Alumni, BaseCalendarEvent, Notification, UniversityAdmission, UserAction, AlumniCollection, IPWhiteList
from .forms import AlumniAdminForm
from .utils import send_birthday_emails


def send_birthday_emails_action(modeladmin, request, queryset):
    result = send_birthday_emails()
    modeladmin.message_user(request, result)

send_birthday_emails_action.short_description = 'Send Birthday Emails to Admin'


class AlumniInline(admin.TabularInline):
    model = Alumni
    extra = 1

class AlumniCollectionInline(admin.TabularInline):
    model = AlumniCollection
    extra = 1
    readonly_fields = ['view_alumni_collection_link']

    def view_alumni_collection_link(self, obj):
        link = reverse("admin:alumni_alumnicollection_change", args=[obj.id])  # replace 'yourapp' with your app's name
        return format_html('<a href="{}">View</a>', link)

    view_alumni_collection_link.short_description = "View Alumni Collection"

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [AlumniCollectionInline]

class AlumniCollectionAdmin(admin.ModelAdmin):
    list_display = ['year', 'school']
    search_fields = ['year', 'school__name']
    inlines = [AlumniInline]
    list_filter = ['year', 'school__name']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            alumni_query = Alumni.objects.filter(
                name__icontains=search_term
            )
            queryset |= self.model.objects.filter(alumni__in=alumni_query).distinct()
        except Exception as e:
            self.message_user(request, f"Error while searching: {e}", level='error')
        return queryset, use_distinct

class AlumniAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'graduate_year', 
        'school',
        'birthday',
        'class_number', 
        'major', 
        'location', 
        'education_info', 
        'current_job', 
        'GBT', 
        'interaction_status', 
        'description', 
        'military_status', 
        'city', 
        'marital_status',
    ]
    search_fields = [
        'name', 
        'birthday',
        'graduate_year', 
        'school', 
        'class_number', 
        'major', 
        'location', 
        'education_info', 
        'current_job', 
        'GBT', 
        'interaction_status', 
        'description', 
        'military_status', 
        'city', 
        'marital_status',
    ]
    list_filter=[
        #'name', 
        #'birthday',
        'graduate_year', 
        'school', 
        'class_number', 
        'major', 
        'location', 
        #'education_info', 
        'current_job', 
        'GBT', 
        'interaction_status', 
        #'description', 
        'military_status', 
        'city', 
        'marital_status',
    ]
    ordering = ['graduate_year', 'school']

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']
    list_filter = ['user', 'action']
    search_fields = ['user__email', 'action', 'timestamp']
    ordering = ['-timestamp']

admin.site.register(School, SchoolAdmin)
admin.site.register(AlumniCollection, AlumniCollectionAdmin)
admin.site.register(Alumni, AlumniAdmin)
admin.site.register(BaseCalendarEvent)
admin.site.register(UniversityAdmission)
admin.site.register(IPWhiteList)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'timestamp']
    filter_horizontal = ['recipients', 'read_by']

