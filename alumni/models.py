# alumni/models.py

from django.db import models
from django.utils import timezone
from django.db.models.base import ModelBase
from calendarapp.models import Event
from django.conf import settings


class IPWhiteList(models.Model):
    ip_address = models.CharField(max_length=200)


    def __str__(self):
        return self.ip_address

class BaseCalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=False)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notifications')
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='read_notifications')
    
    def __str__(self):
        return self.message
    
    def mark_as_read(self, user):
        self.read_by.add(user)
        self.save()

    def is_read_by(self, user):
        return user in self.read_by.all()



class School(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Delete associated alumni and their events when deleting a school
        for alumni in self.alumni_collections.all():
            alumni.delete()
        super().delete(*args, **kwargs)

class AlumniCollection(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='alumni_collections')
    year = models.PositiveIntegerField(default = 1997)

    def __str__(self):
        return str(self.year)

    def delete(self, *args, **kwargs):
        # Delete associated alumni and their events when deleting an alumni collection
        for alumni in self.alumni.all():
            alumni.delete()

        super().delete(*args, **kwargs)

class Alumni(models.Model):
    alumni_collection = models.ForeignKey(AlumniCollection, on_delete=models.CASCADE, related_name='alumni', default=None, null=True)
    name = models.CharField(max_length=100, default="unknown")
    birthday = models.DateField(default="unknown")
    graduate_year = models.IntegerField(default=2020)  
    school = models.CharField(max_length=500, default="unknown")
    class_number = models.CharField(max_length=10, default="A")
    #notes = models.CharField(max_length=10, default="", null=True)
    major = models.CharField(max_length=30, default="Biology")
    #social_media = models.CharField(max_length=500, default="unknown")
    location = models.CharField(max_length=300, default='Turkmenistan')
    education_info = models.TextField(default='None') #will hold education degree or info about their education
    current_job = models.TextField(default='None') #will hold current job info or current position info 
    #email = models.EmailField(default="unknown")
    GBT = models.IntegerField(default="0")
    interaction_status = models.IntegerField(default="0")
    description = models.TextField(default='No description available') # brief little description about the student
    
    MILITARY_CATEGORIES = [
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
        ('future', 'Future'),
    ]

    MARRIED_CATEGORIES = [
        ('not married', 'Not Married'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    ]
    

    military_status = models.CharField(max_length=20, choices=MILITARY_CATEGORIES, default='future')
    city = models.CharField(max_length=25, default='Los Angeles')
    marital_status = models.CharField(max_length=20, choices=MARRIED_CATEGORIES, default='not married')

    def delete(self, *args, **kwargs):
        # Delete associated birthday events when deleting an alumni
        name_pattern = f"{self.name}"
        Event.objects.filter(
            title__icontains=name_pattern,
        ).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
    
class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserAction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, blank=True)
    show_name = models.BooleanField(default=True)
    show_school = models.BooleanField(default=False)
    show_graduate_year = models.BooleanField(default=True)
    show_birthday = models.BooleanField(default=False)
    show_socials = models.BooleanField(default=False)
    show_location = models.BooleanField(default=False)
    show_education = models.BooleanField(default=False)
    show_current_job = models.BooleanField(default=False)
    show_email = models.BooleanField(default=False)
    show_military = models.BooleanField(default=False)
    show_marital = models.BooleanField(default=False)

    # Add fields for other columns as needed


class AlumniGroup(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='alumni_groups')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class TrackRecord(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='track_records')
    record = models.TextField()
    date = models.DateField(default=timezone.now)  # Provide a default value

    def __str__(self):
        return self.record


class UniversityAdmission(models.Model):
    name = models.TextField()
    location = models.TextField()
    link_to_admissions = models.TextField()

    def __str__(self):
        return self.name
    
class UserNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.notification.id} for User {self.user.email}"