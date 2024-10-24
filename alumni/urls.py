# alumni/urls.py

from django.urls import path
from . import views


app_name = 'alumni'

urlpatterns = [
    #path('notifications/', views.view_notifications, name='notifs'),
    path('universities/', views.university_list, name='universities'),
    path('schools/', views.school_list, name='school_list'),
    path('schools/add/', views.add_school, name='add_school'),
    path('schools/<int:school_id>/', views.school_detail, name='school_detail'),
    path('schools/<int:school_id>/delete/', views.delete_school, name='delete_school'),
    path('alumni/alumni_collections/<int:school_id>/add_alumni/', views.add_alumni, name='add_alumni'),
    path('alumni/schools/<int:school_id>/<int:alumni_id>/delete/', views.delete_alumni, name='delete_alumni'),
    path('schools/<int:school_id>/add_track_record/<int:alumni_id>/', views.add_track_record, name='add_track_record'),  # Updated URL pattern for adding a track recordschool_id parameter
    path('schools/<int:school_id>/add_alumni_collection/', views.add_alumni_collection, name='add_alumni_collection'),
    path('alumni_collections/<int:collection_id>/', views.view_alumni_collection, name='view_alumni_collection'),  # New URL pattern for viewing alumni collection
    path('alumni/<int:alumni_id>/', views.view_alumni, name='view_alumni'),  # New URL pat
    path('alumni/<int:alumni_id>/add_track_record/', views.add_track_record, name='add_track_record'),  # Updated URL pattern for adding a track record
    path('alumni/schools/<int:school_id>/<int:alumni_id>/delete_track_record/<int:record_id>/', views.delete_track_record, name='delete_track_record'),
    path('alumni/schools/<int:school_id>/delete_alumni_collection/<int:collection_id>/', views.delete_alumni_collection, name='delete_alumni_collection'),
    path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark_notification_as_unread/<int:notification_id>/', views.mark_notification_as_unread, name='mark_notification_as_unread'),
    path('filter/', views.filter_alumni, name='filter_alumni'),
    path('settings/', views.user_profile_settings, name='column_settings'),
    path('job-openings/', views.job_openings_list, name='job_openings_list'),
    path('create-job-opening/', views.create_job_opening, name='create_job_opening'),
    path('alumni/schools/<int:school_id>/<int:alumni_id>/edit_track_record/<int:record_id>/', views.edit_track_record, name="edit_track_record"),
    path('alumni/alumni_collections/<int:school_id>/edit_alumni/<int:alumni_id>/', views.edit_alumni, name='edit_alumni'),
    path('import-alumni/', views.import_alumni, name='import_alumni'),
    path('export-alumni/<int:school_id>', views.export_alumni, name='export_alumni'),
]
