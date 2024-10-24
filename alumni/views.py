# alumni/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import School, Alumni, AlumniCollection, TrackRecord, UserAction
from .forms import SchoolForm, AlumniForm, TrackRecordForm, AlumniCollectionForm, AlumniFilterForm, JobOpeningForm
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db import models
from django.contrib.auth.models import User
from calendarapp.models import Event
from django.utils import timezone
from .models import Notification, UniversityAdmission, JobOpening
from django.template.loader import render_to_string
from django.utils import timezone
from .utils import generate_notifications_for_upcoming_events
import datetime
from datetime import date
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from eventcalendar.urls import DashboardView
import json
import pandas as pd
from .forms import CSVUploadForm
import csv
from django.utils.encoding import smart_str
from django.contrib import messages

import chardet


# Your existing views...
def bell_icon_data(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipients=request.user).order_by('-timestamp')
        unread_notifications = notifications.exclude(read_by=request.user)
    else:
        unread_notifications = None

    context = {'unread_notifications': unread_notifications}
    return render(request, 'b.html', context)


# View to display job openings
def job_openings_list(request):
    job_openings = JobOpening.objects.all()
    return render(request, 'alumni/job_openings_list.html', {'job_openings': job_openings})

# View to create a job opening
@login_required
def create_job_opening(request):
    if request.method == 'POST':
        form = JobOpeningForm(request.POST)
        if form.is_valid():
            job_opening = form.save(commit=False)
            job_opening.created_by = request.user
            job_opening.save()
            action_description = f"{request.user} posted a job."
            UserAction.objects.create(
                user=request.user,  # User who performed the action
                action=action_description,  # Description of the action
            )
            return redirect('alumni:job_openings_list')  # Redirect back to the job openings list

    else:
        form = JobOpeningForm()

    return render(request, 'alumni/create_job_opening.html', {'form': form})

def user_profile_settings(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('alumni:school_list')

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'alumni/user_profile_settings.html', {'form': form})




def view_alumni(request, alumni_id):
    alumnus = get_object_or_404(Alumni, id=alumni_id)

    return render(request, 'alumni/view_alumni.html', {'alumnus': alumnus})




def view_alumni_collection(request, collection_id):
    collection = get_object_or_404(AlumniCollection, id=collection_id)
    alumni = collection.alumni.all()

    alumni_per_page = 20
    paginator = Paginator(alumni, alumni_per_page)  # 20 alumni per page

    # Get the current page number from the request's GET parameters (default to 1 if not provided)
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, 'alumni/view_alumni_collection.html', {'collection': collection, 'alumni': alumni, 'page': page})    

def add_alumni_collection(request, school_id):
    school = get_object_or_404(School, id=school_id)

    if request.method == 'POST':
        form = AlumniCollectionForm(request.POST)
        if form.is_valid():
            alumni_collection = form.save(commit=False)
            alumni_collection.school = school
            alumni_collection.save()
            action_description = f"{request.user} created a new alumni collection in {alumni_collection.school}."
            UserAction.objects.create(
                user=request.user,  # User who performed the action
                action=action_description,  # Description of the action
            )
            for reunion_year in [5, 10, 15]:
                event_year = alumni_collection.year + reunion_year
                event_date = date(event_year, 5, 25)
                event_title = f"{alumni_collection.school} Reunion {reunion_year} Years for class of {alumni_collection.year}!"
                Event.objects.create(
                    user=request.user,
                    title=event_title,
                    description=f"It is the {reunion_year}-year reunion!",
                    start_time=event_date,
                    end_time=event_date,
                )
            return redirect('alumni:school_detail', school_id=school_id)


    else:
        form = AlumniCollectionForm()

    return render(request, 'alumni/add_alumni_collection.html', {'form': form, 'school': school})


def add_track_record(request, school_id, alumni_id):
    alumnus = get_object_or_404(Alumni, id=alumni_id, alumni_collection__school_id=school_id)

    if request.method == 'POST':
        form = TrackRecordForm(request.POST)
        if form.is_valid():
            track_record = form.save(commit=False)
            track_record.alumni = alumnus  # Set the alumni for the track record
            track_record.save()
            action_description = f"{request.user} added a track record for {track_record.alumni}"
            UserAction.objects.create(
                user=request.user,  # User who performed the action
                action=action_description,  # Description of the action
            )
            return redirect('alumni:view_alumni', alumni_id=alumnus.id)
    else:
        form = TrackRecordForm()

    return render(request, 'alumni/add_track_record.html', {'form': form, 'alumnus': alumnus})

def delete_track_record(request, school_id, alumni_id, record_id):
    alumni = get_object_or_404(Alumni, id=alumni_id)
    record = get_object_or_404(TrackRecord, id=record_id)

    if request.method == 'POST':
        action_description = f"{request.user} deleted a track record for {alumni}"
        UserAction.objects.create(
            user=request.user,  # User who performed the action
            action=action_description,  # Description of the action
        )
        record.delete()
        return redirect('alumni:view_alumni', alumni_id=alumni_id)

    context = {
        'alumni': alumni,
        'record': record,
        'school_id': school_id,
    }
    return render(request, 'alumni/delete_track_record.html', context)

def edit_track_record(request, school_id, alumni_id, record_id):
    alumni = get_object_or_404(Alumni, id=alumni_id)


    record = get_object_or_404(TrackRecord, id=record_id)
    form = TrackRecordForm(instance=record)
    if request.method == 'POST':
            form = TrackRecordForm(request.POST, instance=record)
            if form.is_valid():
                form.save()

                action_description = f"{request.user} edited a track record for {alumni}"
                UserAction.objects.create(
                    user=request.user,  # User who performed the action
                    action=action_description,  # Description of the action
                )
                return redirect('alumni:view_alumni', alumni_id=alumni_id)

    context = {
        'alumni': alumni,
        'record': record,
        'school_id': school_id,
        'form' : form,
    }
    return render(request, 'alumni/edit_track_record.html', context)

"""
def edit_alumni(request, school_id, alumni_id):
    school = get_object_or_404(School, id=school_id)
    alumni = get_object_or_404(Alumni, id=alumni_id)

    if request.method == 'POST':
        form = AlumniForm(request.POST, instance=alumni, school=school)
        if form.is_valid():
            edited_alumni = form.save(commit=False)
            edited_alumni.school = school.name
            edited_alumni.save()

            action_description = f"{request.user} edited alumni details for {alumni}"
            UserAction.objects.create(
                user=request.user,
                action=action_description,
            )


            return redirect('alumni:school_detail', school_id=school.id)
    else:
        form = AlumniForm(instance=alumni, school=school)

    context = {
        'form': form,
        'school': school,
        'alumni': alumni,
    }
    return render(request, 'alumni/edit_alumni.html', context)
"""

def edit_alumni(request, school_id, alumni_id):
    school = get_object_or_404(School, id=school_id)
    alumni = get_object_or_404(Alumni, id=alumni_id)

    #for the DigitalOcean server do:
    #if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Retrieve data from the AJAX request
        data = json.loads(request.body)
        alumni.name = data.get('name', '')
        
        # Update other fields based on your model
        alumni.birthday = data.get('birthday', '')
        alumni.location = data.get('location', '') 
        alumni.city = data.get('city', '')
        alumni.GBT = data.get('gbt', '')
        alumni.interaction_status = data.get('interaction_status', '')
        alumni.class_number = data.get('class_number', '')
        alumni.major = data.get('major', '')
        alumni.education_info = data.get('education', '') # doesn't work for editing
        alumni.description = data.get('description', '')
        alumni.current_job = data.get('current_job', '')
        alumni.military_status = data.get('military_status', '') # doesn't work for editing
        alumni.marital_status = data.get('marital_status', '')
        
        # ... add similar lines for other fields

        print("We have received the POST request")
        alumni.save()

        action_description = f"{request.user} edited alumni details for {alumni}"
        UserAction.objects.create(
            user=request.user,
            action=action_description,
        )

        return JsonResponse({'status': 'success'})
    else:
        print("we have NOT gotten the POST request")

    context = {
        'school': school,
        'alumni': alumni,
    }
    return render(request, 'alumni/edit_alumni.html', context)


def school_list(request):
    print(request.user) 
    schools = School.objects.filter(user = request.user)

    # Set the number of schools per page
    schools_per_page = 20
    paginator = Paginator(schools, schools_per_page)

    # Get the current page number from the request's GET parameter (default to 1 if not provided)
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    return render(request, 'alumni/school_list.html', {'page': page})

def add_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.user = request.user
            school.save()
            action_description = f"{request.user} created a new school."
            UserAction.objects.create(
                user=request.user,  # User who performed the action
                action=action_description,  # Description of the action
            )
            return redirect('alumni:school_list')
    else:
        form = SchoolForm()
    return render(request, 'alumni/add_school.html', {'form': form})

def delete_school(request, school_id):
    school = get_object_or_404(School, id=school_id)
    if request.method == 'POST':
        school.delete()
        return redirect('alumni:school_list')
    return render(request, 'alumni/delete_school.html', {'school': school})

def add_alumni(request, school_id):
    school = get_object_or_404(School, id=school_id)
    if request.method == 'POST':
        form = AlumniForm(request.POST, school=school)
        if form.is_valid():
            alumni = form.save(commit=False)
            alumni.school = alumni.alumni_collection.school
            alumni.save()
            action_description = f"{request.user} added {alumni.name} to school: {alumni.school}"
            UserAction.objects.create(
                user=request.user,  # User who performed the action
                action=action_description,  # Description of the action
            )
            name = alumni.name
            birthday = alumni.birthday
            year = datetime.datetime.now().year
            same_year = year
            while year < (same_year + 1):
                event_date = date(year, alumni.birthday.month, alumni.birthday.day)
                event_title = f"{name}'s Birthday {event_date}"  # Append year to the title
                Event.objects.create(
                    user=request.user,
                    title=event_title,
                    description=f"It is {name}'s birthday today! + {event_date}",
                    start_time=event_date,
                    end_time=event_date,
                )
                year += 1
            return redirect('alumni:school_detail', school_id=alumni.school.id)
    else:
        form = AlumniForm(school=school)

    context = {
        'form': form,
        'school':school,
    }
    return render(request, 'alumni/add_alumni.html', context)

def delete_alumni(request, school_id, alumni_id):
    alumni = get_object_or_404(Alumni, id=alumni_id)
    if request.method == 'POST':
        alumni.delete()
        return redirect('alumni:view_alumni_collection', collection_id=alumni.alumni_collection.id)
    context = {
        'alumni': alumni,
        'school_id': school_id,
    }
    return render(request, 'alumni/delete_alumni.html', context)



def school_detail(request, school_id):
    school = get_object_or_404(School, id=school_id)
    alumnis_for_first_page = Alumni.objects.filter(school = school)
    alumni_count = alumnis_for_first_page.count()
    return render(request, 'alumni/school_detail.html', {'school': school, 'alumnis_for_first_page': alumnis_for_first_page, 'alumni_count': alumni_count})

def delete_alumni_collection(request, school_id, collection_id):
    collection = get_object_or_404(AlumniCollection, id=collection_id)
    school = get_object_or_404(School, id=school_id)

    if request.method == 'POST':
        collection.delete()
        return redirect('alumni:school_detail', school_id=school_id)

    context = {
        'collection': collection,
        'school': school,
    }
    return render(request, 'alumni/delete_alumni_collection.html', context)


def view_notifications(request):
    # Query all notifications for the current user
    notifications = Notification.objects.filter(recipients=request.user).order_by('-timestamp')

    unread_notifications = notifications.filter(read_by=request.user)
    read_notifications = notifications.exclude(read_by=request.user)
    return render(request, 'alumni/notifications.html', {'notifications': notifications, 'unread_notifications': unread_notifications, 'read_notifications': read_notifications})

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)

    # Check if the notification belongs to the logged-in user
    if request.user in notification.recipients.all():
        # Mark the notification as read by the current user
        notification.mark_as_read(request.user)
        action_description = f"{request.user} marked a notification as read."
        UserAction.objects.create(
            user=request.user,  # User who performed the action
            action=action_description,  # Description of the action
        )
        return redirect('dashboard')
    else:
        return HttpResponseForbidden("You don't have permission to mark this notification as read.")

# Mark a notification as unread
def mark_notification_as_unread(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)

    # Check if the notification belongs to the logged-in user
    if request.user in notification.recipients.all():
        # Remove the current user from the list of users who have read the notification
        notification.read_by.remove(request.user)
        return redirect('dashboard')
    else:
        return HttpResponseForbidden("You don't have permission to mark this notification as unread.")

def university_list(request):
    universities = UniversityAdmission.objects.all()

    return render(request, 'alumni/university_list.html', {'universities': universities})

def filter_alumni(request):
    alumni = Alumni.objects.all()
    form = AlumniFilterForm(request.GET)

    if form.is_valid():
        school = form.cleaned_data['school']
        graduate_year = form.cleaned_data['graduate_year']
        name = form.cleaned_data['name']

        if school:
            alumni = alumni.filter(alumni_collection__school=school)

        if graduate_year:
            alumni = alumni.filter(graduate_year=graduate_year)

        if name:  # Filter by name if provided
            alumni = alumni.filter(name__icontains=name)

    return render(request, 'alumni/filter_results.html', {'alumni': alumni, 'form': form})

from pandas.errors import EmptyDataError
from datetime import datetime as import_dt
import chardet
import io
def import_alumni(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Detect the file encoding
            raw_data = csv_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            csv_file.seek(0)  # Reset the file pointer to the beginning

            # Convert to UTF-8 encoding
            try:
                decoded_data = raw_data.decode(encoding)
                utf8_data = decoded_data.encode('utf-8')
                csv_file = io.BytesIO(utf8_data)
            except UnicodeDecodeError as e:
                return HttpResponse(f"UnicodeDecodeError: {e}")

            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
            except EmptyDataError:
                return HttpResponse("The uploaded CSV file is empty.")
            except UnicodeDecodeError as e:
                return HttpResponse(f"UnicodeDecodeError: {e}")

            for index, row in df.iterrows():
                graduate_year = row['graduate_year']
                school_name = row['school']
                school, _ = School.objects.get_or_create(name=school_name)
                alumni_collection, _ = AlumniCollection.objects.get_or_create(
                    school=school,
                    year=graduate_year
                )
                birthday_str = row['birthday']
                try:
                    birthday_date = import_dt.strptime(birthday_str, '%m/%d/%Y').date()
                except ValueError:
                    birthday_date = None
                Alumni.objects.create(
                    alumni_collection=alumni_collection,
                    name=row['name'],
                    birthday=birthday_date,
                    graduate_year=row['graduate_year'],
                    school=row['school'],
                    class_number=row['class_number'],
                    major=row['major'],
                    location=row['location'],
                    education_info=row['education_info'],
                    current_job=row['current_job'],
                    GBT=row['gbt'],
                    interaction_status=row['interaction_status'],
                    description=row['description'],
                    military_status=row['military'],
                    city=row['city'],
                    marital_status=row['marital'],
                )
            return redirect('alumni:school_list')
    else:
        form = CSVUploadForm()
    return render(request, 'alumni/import.html', {'form': form})

def export_alumni(request, school_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumni.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow([
        'name', 'birthday', 'graduate_year', 'school', 'class_number', 'major',
        'city', 'location', 'education_info', 'current_job', 'gbt', 
        'interaction_status', 'description', 'military', 'marital'
    ])

    # Query alumni data
    alumni = Alumni.objects.filter(alumni_collection__school_id=school_id)

    # Write alumni data to CSV
    for alumni_member in alumni:
        # Manually encode string fields as UTF-8
        writer.writerow([
            alumni_member.name.encode('utf-8').decode('utf-8') if isinstance(alumni_member.name, str) else alumni_member.name,
            alumni_member.birthday.encode('utf-8').decode('utf-8') if isinstance(alumni_member.birthday, str) else alumni_member.birthday,
            alumni_member.graduate_year.encode('utf-8').decode('utf-8') if isinstance(alumni_member.graduate_year, str) else alumni_member.graduate_year,
            alumni_member.school.encode('utf-8').decode('utf-8') if isinstance(alumni_member.school, str) else alumni_member.school,
            alumni_member.class_number,
            alumni_member.major.encode('utf-8').decode('utf-8') if isinstance(alumni_member.major, str) else alumni_member.major,
            alumni_member.city.encode('utf-8').decode('utf-8') if isinstance(alumni_member.city, str) else alumni_member.city,
            alumni_member.location.encode('utf-8').decode('utf-8') if isinstance(alumni_member.location, str) else alumni_member.location,
            alumni_member.education_info.encode('utf-8').decode('utf-8') if isinstance(alumni_member.education_info, str) else alumni_member.education_info,
            alumni_member.current_job.encode('utf-8').decode('utf-8') if isinstance(alumni_member.current_job, str) else alumni_member.current_job,
            alumni_member.GBT.encode('utf-8').decode('utf-8') if isinstance(alumni_member.GBT, str) else alumni_member.GBT,
            alumni_member.interaction_status.encode('utf-8').decode('utf-8') if isinstance(alumni_member.interaction_status, str) else alumni_member.interaction_status,
            alumni_member.description.encode('utf-8').decode('utf-8') if isinstance(alumni_member.description, str) else alumni_member.description,
            alumni_member.military_status.encode('utf-8').decode('utf-8') if isinstance(alumni_member.military_status, str) else alumni_member.military_status,
            alumni_member.marital_status.encode('utf-8').decode('utf-8') if isinstance(alumni_member.marital_status, str) else alumni_member.marital_status,
        ])

    return response